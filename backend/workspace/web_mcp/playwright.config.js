const { defineConfig, devices } = require('@playwright/test');

// 智能判断是否使用 headed 模式：
// - 环境变量 PW_HEADED=1 强制 headed
// - 有 DISPLAY 环境变量（真实桌面环境）时用 headed
// - 否则（Docker 无显示器）自动用 headless
const hasDisplay = !!process.env.DISPLAY;
const forceHeaded = process.env.PW_HEADED === '1';
const useHeaded = forceHeaded || hasDisplay;

console.log(`[Playwright Config] headless=${!useHeaded} (DISPLAY=${process.env.DISPLAY || 'none'}, PW_HEADED=${process.env.PW_HEADED || 'not-set'})`);

module.exports = defineConfig({
  testDir: './tests',
  timeout: 300000, // 5分钟超时
  expect: {
    timeout: 30000
  },
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: 'html',
  use: {
    trace: 'on-first-retry',
    video: 'on',  // 启用视频录制
    videoSize: { width: 1280, height: 720 },
    headless: !useHeaded,  // 有显示器时显示窗口，否则无头执行
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  outputDir: 'test-results',  // 视频和trace输出目录
});
