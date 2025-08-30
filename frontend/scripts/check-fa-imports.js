#!/usr/bin/env node

/**
 * Preventive check script to detect react-icons/fa imports
 * This script fails the build if any fa imports are found
 * Usage: node scripts/check-fa-imports.js
 */

const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, '..', 'src');
const extensions = ['.tsx', '.ts', '.jsx', '.js'];

function findFiles(dir, extensions) {
  let files = [];
  
  const items = fs.readdirSync(dir);
  
  for (const item of items) {
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory()) {
      // Skip node_modules and .next directories
      if (item !== 'node_modules' && item !== '.next') {
        files = files.concat(findFiles(fullPath, extensions));
      }
    } else if (extensions.some(ext => item.endsWith(ext))) {
      files.push(fullPath);
    }
  }
  
  return files;
}

function checkFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const lines = content.split('\n');
  const violations = [];
  
  lines.forEach((line, index) => {
    if (line.includes('react-icons/fa') && !line.includes('react-icons/fa6')) {
      violations.push({
        file: filePath,
        line: index + 1,
        content: line.trim()
      });
    }
  });
  
  return violations;
}

function main() {
  console.log('🔍 Checking for react-icons/fa imports...');
  
  const files = findFiles(srcDir, extensions);
  let allViolations = [];
  
  for (const file of files) {
    const violations = checkFile(file);
    allViolations = allViolations.concat(violations);
  }
  
  if (allViolations.length > 0) {
    console.error('❌ Found react-icons/fa imports (should be react-icons/fa6):');
    console.error('');
    
    allViolations.forEach(violation => {
      const relativePath = path.relative(process.cwd(), violation.file);
      console.error(`  ${relativePath}:${violation.line}`);
      console.error(`    ${violation.content}`);
      console.error('');
    });
    
    console.error('💡 Fix: Replace "react-icons/fa" with "react-icons/fa6"');
    process.exit(1);
  } else {
    console.log('✅ No react-icons/fa imports found');
  }
}

if (require.main === module) {
  main();
}

module.exports = { findFiles, checkFile };