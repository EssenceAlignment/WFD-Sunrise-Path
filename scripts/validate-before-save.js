const fs = require('fs');
const path = require('path');

class MarkdownValidator {
  constructor() {
    this.errors = [];
  }

  validateMarkdownFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');

    this.checkHeadingSpacing(lines);
    this.checkCodeBlockSpacing(lines);
    this.checkCodeBlockLanguages(lines);

    return this.errors;
  }

  checkHeadingSpacing(lines) {
    lines.forEach((line, index) => {
      if (line.match(/^#{1,6}\s+/)) {
        // Check line before heading (if not first line)
        if (index > 0 && lines[index - 1].trim() !== '') {
          this.errors.push({
            line: index + 1,
            type: 'MD022',
            message: 'Heading needs blank line before'
          });
        }

        // Check line after heading (if not last line)
        if (index < lines.length - 1 && lines[index + 1].trim() !== '') {
          this.errors.push({
            line: index + 1,
            type: 'MD022',
            message: 'Heading needs blank line after'
          });
        }
      }
    });
  }

  checkCodeBlockSpacing(lines) {
    lines.forEach((line, index) => {
      if (line.startsWith('```')) {
        // Opening fence
        if (!line.endsWith('```')) {
          if (index > 0 && lines[index - 1].trim() !== '') {
            this.errors.push({
              line: index + 1,
              type: 'MD031',
              message: 'Code block needs blank line before'
            });
          }
        }

        // Closing fence
        if (line === '```') {
          if (index < lines.length - 1 && lines[index + 1].trim() !== '') {
            this.errors.push({
              line: index + 1,
              type: 'MD031',
              message: 'Code block needs blank line after'
            });
          }
        }
      }
    });
  }

  checkCodeBlockLanguages(lines) {
    lines.forEach((line, index) => {
      if (line === '```') {
        // Find if this is an opening fence by checking for closing
        let isOpening = false;
        for (let i = index + 1; i < lines.length; i++) {
          if (lines[i].startsWith('```')) {
            isOpening = true;
            break;
          }
        }

        if (isOpening) {
          this.errors.push({
            line: index + 1,
            type: 'MD040',
            message: 'Code block missing language identifier'
          });
        }
      }
    });
  }
}

// Auto-fix function
function autoFixMarkdown(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');

  // Fix headings spacing
  content = content.replace(/([^\n])\n(#{1,6}\s+)/g, '$1\n\n$2');
  content = content.replace(/(#{1,6}\s+.+)\n([^\n])/g, '$1\n\n$2');

  // Fix code block spacing
  content = content.replace(/([^\n])\n(```)/g, '$1\n\n$2');
  content = content.replace(/(```)\n([^\n])/g, '$1\n\n$2');

  // Fix missing languages (detect and add)
  content = content.replace(/\n```\n/g, (match, offset) => {
    const afterFence = content.substring(offset + match.length, offset + match.length + 100);

    if (afterFence.includes('const ') || afterFence.includes('function ')) {
      return '\n```javascript\n';
    } else if (afterFence.includes('echo ') || afterFence.includes('#!/bin/bash')) {
      return '\n```bash\n';
    } else if (afterFence.match(/^\s*{/)) {
      return '\n```json\n';
    } else if (afterFence.match(/^\s*\w+:/)) {
      return '\n```yaml\n';
    } else {
      return '\n```text\n';
    }
  });

  fs.writeFileSync(filePath, content);
}

module.exports = { MarkdownValidator, autoFixMarkdown };
