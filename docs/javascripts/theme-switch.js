document.addEventListener('DOMContentLoaded', function() {
  // 获取系统主题偏好
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

  // 监听系统主题变化
  prefersDark.addListener((e) => {
    const theme = e.matches ? 'slate' : 'default';
    document.body.setAttribute('data-md-color-scheme', theme);
  });

  // 初始化主题
  const theme = prefersDark.matches ? 'slate' : 'default';
  document.body.setAttribute('data-md-color-scheme', theme);
});