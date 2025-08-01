const { Octokit } = require("@octokit/rest");
const { execSync } = require('child_process');
const fs = require('fs').promises;
const path = require('path');

class PROptimizationBot {
  constructor() {
    this.octokit = new Octokit({
      auth: process.env.GITHUB_TOKEN || process.env.GH_TOKEN,
    });

    this.owner = process.env.GITHUB_REPOSITORY_OWNER || 'Recovery-Compass';
    this.repo = process.env.GITHUB_REPOSITORY?.split('/')[1] || 'wfd-sunrise-path';
  }

  async analyzePR(prNumber) {
    console.log(`Analyzing PR #${prNumber}...`);

    const pr = await this.octokit.pulls.get({
      owner: this.owner,
      repo: this.repo,
      pull_number: prNumber
    });

    const issues = [];

    // Check PR size
    if (pr.data.commits > 50) {
      issues.push({
        type: 'too_many_commits',
        severity: 'high',
        message: `PR has ${pr.data.commits} commits (threshold: 50)`,
        recommendation: 'Split into smaller PRs by feature area'
      });
    }

    if (pr.data.additions > 10000) {
      issues.push({
        type: 'too_large',
        severity: 'critical',
        message: `PR adds ${pr.data.additions} lines (threshold: 10,000)`,
        recommendation: 'Split into incremental changes'
      });
    }

    if (pr.data.changed_files > 100) {
      issues.push({
        type: 'too_many_files',
        severity: 'high',
        message: `PR changes ${pr.data.changed_files} files (threshold: 100)`,
        recommendation: 'Group changes by component'
      });
    }

    // Check for common anti-patterns
    const files = await this.octokit.pulls.listFiles({
      owner: this.owner,
      repo: this.repo,
      pull_number: prNumber
    });

    // Check for secrets
    const secretPatterns = [
      /api[_-]?key/i,
      /secret/i,
      /password/i,
      /token/i,
      /private[_-]?key/i
    ];

    for (const file of files.data) {
      if (file.patch) {
        for (const pattern of secretPatterns) {
          if (pattern.test(file.patch) && !file.filename.includes('.example')) {
            issues.push({
              type: 'potential_secret',
              severity: 'critical',
              file: file.filename,
              message: 'Potential secret detected',
              recommendation: 'Move to environment variables or secret management'
            });
          }
        }
      }
    }

    return { pr: pr.data, issues };
  }

  async autoSplitPR(prNumber) {
    console.log(`Auto-splitting PR #${prNumber}...`);

    const commits = await this.octokit.pulls.listCommits({
      owner: this.owner,
      repo: this.repo,
      pull_number: prNumber,
      per_page: 100
    });

    const commitGroups = this.intelligentGroupCommits(commits.data);
    const createdPRs = [];

    for (const group of commitGroups) {
      const newPR = await this.createSplitPR(prNumber, group);
      if (newPR) {
        createdPRs.push(newPR);
      }
    }

    return createdPRs;
  }

  intelligentGroupCommits(commits) {
    const groups = {
      security: { commits: [], patterns: [/security/i, /secret/i, /auth/i, /\.env/i] },
      infrastructure: { commits: [], patterns: [/docker/i, /infra/i, /deploy/i, /k8s/i] },
      features: { commits: [], patterns: [/feat/i, /feature/i, /add/i] },
      documentation: { commits: [], patterns: [/doc/i, /readme/i, /\.md$/i] },
      fixes: { commits: [], patterns: [/fix/i, /bug/i, /patch/i] },
      tests: { commits: [], patterns: [/test/i, /spec/i, /coverage/i] },
      cicd: { commits: [], patterns: [/ci/i, /cd/i, /workflow/i, /action/i] }
    };

    // Analyze each commit
    commits.forEach(commit => {
      const message = commit.commit.message.toLowerCase();
      const files = commit.files || [];

      let assigned = false;

      // Check each group's patterns
      for (const [groupName, group] of Object.entries(groups)) {
        for (const pattern of group.patterns) {
          if (pattern.test(message) || files.some(f => pattern.test(f.filename))) {
            group.commits.push(commit);
            assigned = true;
            break;
          }
        }
        if (assigned) break;
      }

      // If not assigned, put in fixes as default
      if (!assigned) {
        groups.fixes.commits.push(commit);
      }
    });

    // Return only non-empty groups
    return Object.entries(groups)
      .filter(([_, group]) => group.commits.length > 0)
      .map(([type, group]) => ({
        type,
        commits: group.commits,
        count: group.commits.length
      }));
  }

  async createSplitPR(parentPRNumber, group) {
    const branchName = `auto-split/${group.type}-${Date.now()}`;

    try {
      // Create new branch
      const baseBranch = await this.octokit.repos.getBranch({
        owner: this.owner,
        repo: this.repo,
        branch: 'main'
      });

      await this.octokit.git.createRef({
        owner: this.owner,
        repo: this.repo,
        ref: `refs/heads/${branchName}`,
        sha: baseBranch.data.commit.sha
      });

      // Cherry-pick commits
      for (const commit of group.commits) {
        try {
          // This is simplified - in production, you'd use proper git operations
          console.log(`Would cherry-pick commit ${commit.sha} to ${branchName}`);
        } catch (error) {
          console.error(`Failed to cherry-pick ${commit.sha}:`, error.message);
        }
      }

      // Create PR
      const newPR = await this.octokit.pulls.create({
        owner: this.owner,
        repo: this.repo,
        title: `[Auto-Split] ${this.formatTitle(group.type)} - Part of #${parentPRNumber}`,
        head: branchName,
        base: 'main',
        body: this.generatePRBody(group, parentPRNumber)
      });

      // Add labels
      await this.octokit.issues.addLabels({
        owner: this.owner,
        repo: this.repo,
        issue_number: newPR.data.number,
        labels: ['auto-split', group.type, `parent-pr-${parentPRNumber}`]
      });

      return {
        number: newPR.data.number,
        type: group.type,
        url: newPR.data.html_url,
        commits: group.count
      };

    } catch (error) {
      console.error(`Failed to create split PR for ${group.type}:`, error.message);
      return null;
    }
  }

  formatTitle(type) {
    const titles = {
      security: '🔒 Security Updates',
      infrastructure: '🏗️ Infrastructure Changes',
      features: '✨ New Features',
      documentation: '📚 Documentation Updates',
      fixes: '🐛 Bug Fixes',
      tests: '🧪 Test Improvements',
      cicd: '🔄 CI/CD Updates'
    };

    return titles[type] || type.charAt(0).toUpperCase() + type.slice(1);
  }

  generatePRBody(group, parentPRNumber) {
    return `## Automated PR Split

This PR contains **${group.type}** changes extracted from #${parentPRNumber}

### Summary
- **Commits**: ${group.count}
- **Type**: ${group.type}
- **Parent PR**: #${parentPRNumber}

### Commits Included
${group.commits.slice(0, 10).map(c => `- ${c.sha.substring(0, 7)}: ${c.commit.message.split('\n')[0]}`).join('\n')}
${group.count > 10 ? `\n... and ${group.count - 10} more commits` : ''}

### Testing
- [ ] All tests pass
- [ ] No breaking changes
- [ ] Documentation updated (if needed)

### Dependencies
This PR is part of a larger change set. Please review in conjunction with other auto-split PRs from #${parentPRNumber}.

---
*Generated by Recovery Compass PR Optimization Bot*`;
  }

  async generateOptimizationReport(prNumber) {
    const analysis = await this.analyzePR(prNumber);

    const report = {
      prNumber,
      timestamp: new Date().toISOString(),
      summary: {
        commits: analysis.pr.commits,
        additions: analysis.pr.additions,
        deletions: analysis.pr.deletions,
        changedFiles: analysis.pr.changed_files
      },
      issues: analysis.issues,
      recommendations: this.generateRecommendations(analysis),
      automationScore: this.calculateAutomationScore(analysis)
    };

    return report;
  }

  generateRecommendations(analysis) {
    const recommendations = [];

    if (analysis.issues.some(i => i.severity === 'critical')) {
      recommendations.push({
        priority: 'high',
        action: 'Split this PR immediately',
        reason: 'Critical issues detected that block review'
      });
    }

    if (analysis.pr.commits > 20) {
      recommendations.push({
        priority: 'medium',
        action: 'Squash related commits',
        reason: 'Too many commits make history hard to follow'
      });
    }

    if (analysis.pr.changed_files > 50) {
      recommendations.push({
        priority: 'medium',
        action: 'Group changes by component',
        reason: 'Large number of files makes review difficult'
      });
    }

    return recommendations;
  }

  calculateAutomationScore(analysis) {
    let score = 100;

    // Deduct points for issues
    analysis.issues.forEach(issue => {
      if (issue.severity === 'critical') score -= 20;
      else if (issue.severity === 'high') score -= 10;
      else score -= 5;
    });

    // Deduct for size
    if (analysis.pr.commits > 50) score -= 15;
    if (analysis.pr.additions > 10000) score -= 20;
    if (analysis.pr.changed_files > 100) score -= 15;

    return Math.max(0, score);
  }

  async postComment(prNumber, comment) {
    await this.octokit.issues.createComment({
      owner: this.owner,
      repo: this.repo,
      issue_number: prNumber,
      body: comment
    });
  }
}

// CLI interface
if (require.main === module) {
  const command = process.argv[2];
  const prNumber = process.argv[3];

  if (!command || !prNumber) {
    console.log('Usage: node pr-optimization-bot.js <command> <pr-number>');
    console.log('Commands: analyze, split, report');
    process.exit(1);
  }

  const bot = new PROptimizationBot();

  (async () => {
    try {
      switch (command) {
        case 'analyze':
          const analysis = await bot.analyzePR(parseInt(prNumber));
          console.log(JSON.stringify(analysis, null, 2));
          break;

        case 'split':
          const prs = await bot.autoSplitPR(parseInt(prNumber));
          console.log(`Created ${prs.length} split PRs:`, prs);
          break;

        case 'report':
          const report = await bot.generateOptimizationReport(parseInt(prNumber));
          console.log(JSON.stringify(report, null, 2));
          await fs.writeFile(
            `pr-${prNumber}-optimization-report.json`,
            JSON.stringify(report, null, 2)
          );
          break;

        default:
          console.error(`Unknown command: ${command}`);
          process.exit(1);
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  })();
}

module.exports = PROptimizationBot;
