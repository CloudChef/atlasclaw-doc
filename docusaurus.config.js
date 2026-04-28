// @ts-check

const config = {
  title: 'AtlasClaw Docs',
  tagline: 'Core-first documentation for AtlasClaw',
  favicon: 'img/favicon.ico',

  url: 'https://atlasclaw.ai',
  baseUrl: '/',
  organizationName: 'CloudChef',
  projectName: 'atlasclaw-doc',

  onBrokenLinks: 'throw',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn'
    }
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'zh-CN'],
    localeConfigs: {
      en: { label: 'English' },
      'zh-CN': { label: '简体中文' }
    }
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/',
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/CloudChef/atlasclaw-doc/edit/main/'
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css')
        }
      }
    ]
  ],

  themeConfig: {
    image: 'img/atlasclaw-icon.png',
    navbar: {
      title: 'AtlasClaw',
      logo: {
        alt: 'AtlasClaw',
        src: 'img/atlasclaw-icon.png'
      },
      items: [
        { type: 'docSidebar', sidebarId: 'installationGuide', position: 'left', label: 'Install' },
        { type: 'docSidebar', sidebarId: 'adminGuide', position: 'left', label: 'Admin' },
        { type: 'docSidebar', sidebarId: 'userGuide', position: 'left', label: 'User' },
        { type: 'docSidebar', sidebarId: 'coreReference', position: 'left', label: 'Core' },
        { type: 'docSidebar', sidebarId: 'providerIntegration', position: 'left', label: 'Provider Integration' },
        { type: 'docSidebar', sidebarId: 'reference', position: 'left', label: 'Reference' },
        { type: 'localeDropdown', position: 'right' },
        { href: 'https://github.com/CloudChef/atlasclaw', label: 'GitHub', position: 'right' }
      ]
    },
    footer: {
      style: 'light',
      links: [
        {
          title: 'Docs',
          items: [
            { label: 'Installation', to: '/manuals/installation/' },
            { label: 'Administrator Guide', to: '/manuals/administrator/' },
            { label: 'User Guide', to: '/manuals/user/' }
          ]
        },
        {
          title: 'Core',
          items: [
            { label: 'Architecture', to: '/core/architecture' },
            { label: 'Auth and RBAC', to: '/core/auth-and-rbac' },
            { label: 'Channels', to: '/core/channels' }
          ]
        },
        {
          title: 'Providers',
          items: [
            { label: 'Provider Integration', to: '/provider-integration/overview' },
            { label: 'SmartCMP', to: '/provider-integration/smartcmp/overview' }
          ]
        }
      ],
      copyright: `Copyright © ${new Date().getFullYear()} CloudChef.`
    },
    prism: {
      additionalLanguages: ['bash', 'json', 'python']
    }
  }
}

module.exports = config
