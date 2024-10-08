import { uniqueId } from 'lodash'

/**
 * @description 给菜单数据补充上 path 字段
 * @description https://github.com/d2-projects/d2-admin/issues/209
 * @param {Array} menu 原始的菜单数据
 */
function supplementPath (menu) {
  return menu.map(e => ({
    ...e,
    path: e.path || uniqueId('d2-menu-empty-'),
    ...e.children ? {
      children: supplementPath(e.children)
    } : {}
  }))
}

export const menuHeader = supplementPath([
  { path: '/index', title: '首页', icon: 'home' },
  {
    title: 'AI图像处理',
    icon: 'image',
    children: [
      { path: '/page1', title: '文生图', icon: 'text' },
      { path: '/page2', title: '高清修复', icon: 'text' },
      { path: '/page3', title: '图片放大', icon: 'text' }
    ]
  }
])

export const menuAside = supplementPath([
  { path: '/index', title: '首页', icon: 'home' },
  {
    title: 'AI图像处理',
    icon: 'image',
    children: [
      { path: '/page1', title: '文生图', icon: 'text' },
      { path: '/page2', title: '高清修复', icon: 'text' },
      { path: '/page3', title: '图片放大', icon: 'text' }
    ]
  }
])
