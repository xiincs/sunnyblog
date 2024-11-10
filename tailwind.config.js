/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'page-background': '#f5f5f5',
        // 用于突出显示的主色调
        'primary-color': '#3490dc',
        // 辅助颜色，可用于按钮悬停等状态
        'secondary-color': '#ff6b6b',
        // 新添加的颜色，可根据具体需求调整
        'article-title-color': '#2c3e50',
        'input-border-color': '#ced4da',
        'button-bg-color': '#3490dc',
        'button-hover-color': '#2980b9',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      boxShadow: {
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        // 用于表单元素等的轻微阴影
        'form-element-shadow': '0 2px 4px -1px rgba(0, 0, 0, 0.1)',
      },
      borderRadius: {
        // 用于输入框等的圆角
        'input-rounded': '4px',
      },
    },
  },
  plugins: [],
};