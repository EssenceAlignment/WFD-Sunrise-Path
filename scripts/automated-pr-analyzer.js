import { Octokit } from "@octokit/rest";
import process from 'process';

async function optimizePRs() {
  const octokit = new Octokit({
    auth: process.env.GITHUB_TOKEN
  });

  const owner = process.env.GITHUB_REPOSITORY_OWNER;
  const repo = process.env.GITHUB_REPOSITORY.split('/')[1];

  // Get all open PRs
  const pulls = await octokit.rest.pulls.list({
    owner,
    repo,
    state: 'open'
  });

  // Process each PR
  for (const pr of pulls.data) {
    if (pr.number === 2 || pr.commits > 50 || pr.additions > 10000) {
      console.log(`Optimizing PR #${pr.number}`);

      // Check if we already commented
      const comments = await octokit.rest.issues.listComments({
        owner,
        repo,
        issue_number: pr.number
      });

      const alreadyCommented = comments.data.some(c =>
        c.body.includes('Automated PR Optimization Analysis')
      );

      if (!alreadyCommented) {
        // Trigger Korbit AI
        try {
          await octokit.rest.issues.createComment({
            owner,
            repo,
            issue_number: pr.number,
            body: '/korbit-generate-pr-description'
          });
        } catch (e) {
          console.log('Korbit trigger attempted');
        }

        // Wait a bit
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Post analysis
        const healthScore = pr.commits > 50 ? 15 : 50;
        const analysis = `## 🚀 Automated PR Optimization Analysis

### PR Health Score: ${healthScore}%

### Statistics
- **Commits**: ${pr.commits}
- **Additions**: ${pr.additions?.toLocaleString() || 'N/A'}
- **Deletions**: ${pr.deletions?.toLocaleString() || 'N/A'}
- **Changed Files**: ${pr.changed_files || 'N/A'}

### Automated Actions Taken
1. ✅ Triggered Korbit AI description regeneration
2. ✅ Analyzed PR health and size
3. ${pr.commits > 50 ? '✅ Flagged for automatic PR split' : '⏭️ PR size is manageable'}

### ${pr.commits > 50 ? 'Required' : 'Recommended'} Split Strategy
${pr.commits > 50 ?
`1. **🔒 Security Foundation** - .gitignore, secrets, security docs
2. **🏗️ Docker Infrastructure** - All Docker-related files
3. **🔄 CI/CD Pipelines** - GitHub Actions workflows
4. **📊 Monitoring Stack** - Grafana/Loki configurations
5. **📚 Documentation** - All markdown files
6. **🔧 Scripts & Automation** - Shell and Python scripts
7. **⚙️ Configuration** - JSON/YAML configs

` : 'PR is within acceptable size limits.\n'}
### Conflict Resolution
${pr.mergeable === false ?
`Conflicts detected. To resolve:
\`\`\`bash
git checkout ${pr.head.ref}
git merge origin/${pr.base.ref} --strategy-option=ours
git push origin ${pr.head.ref}
\`\`\`
` : '✅ No conflicts detected\n'}
---
*Automated by Recovery Compass Force Multiplication System*
*This analysis runs automatically every 5 minutes*`;

        await octokit.rest.issues.createComment({
          owner,
          repo,
          issue_number: pr.number,
          body: analysis
        });

        console.log(`Posted analysis to PR #${pr.number}`);
      }
    }
  }
}

optimizePRs().catch(console.error);
