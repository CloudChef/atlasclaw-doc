// @ts-check

const sidebars = {
  installationGuide: [
    'manuals/installation/index',
    'manuals/installation/requirements',
    'manuals/installation/install',
    'manuals/installation/configuration',
    'manuals/installation/upgrade'
  ],
  adminGuide: [
    'manuals/administrator/index',
    'manuals/administrator/users-and-roles',
    'manuals/administrator/model-configs',
    'manuals/administrator/provider-instances',
    'manuals/administrator/channel-governance',
    'manuals/administrator/agent-customization',
    'manuals/administrator/troubleshooting'
  ],
  userGuide: [
    'manuals/user/index',
    'manuals/user/conversations',
    'manuals/user/account-settings',
    'manuals/user/provider-tokens',
    'manuals/user/im-channels',
    'manuals/user/permissions'
  ],
  coreReference: [
    'core/architecture',
    'core/auth-and-rbac',
    'core/sessions',
    'core/agents',
    'core/skills-and-tools',
    'core/memory',
    'core/channels',
    'core/hooks-and-heartbeat'
  ],
  providerIntegration: [
    'provider-integration/overview',
    'provider-integration/provider-loading',
    'provider-integration/provider-auth-model',
    'provider-integration/webhook-robot-execution',
    'provider-integration/embedded-mode',
    'provider-integration/embedded-menu-and-floating-ui',
    {
      type: 'category',
      label: 'SmartCMP',
      link: { type: 'doc', id: 'provider-integration/smartcmp/overview' },
      items: [
        'provider-integration/smartcmp/installation',
        'provider-integration/smartcmp/auth-modes',
        'provider-integration/smartcmp/admin-configuration',
        'provider-integration/smartcmp/user-token-setup',
        'provider-integration/smartcmp/capabilities',
        'provider-integration/smartcmp/editor-assistance',
        'provider-integration/smartcmp/request-workflows',
        'provider-integration/smartcmp/approval-workflows',
        'provider-integration/smartcmp/resource-operations',
        'provider-integration/smartcmp/alarm-management',
        'provider-integration/smartcmp/cost-optimization',
        'provider-integration/smartcmp/security-compliance',
        'provider-integration/smartcmp/troubleshooting'
      ]
    }
  ],
  reference: [
    'reference/configuration',
    'reference/api-routes',
    'reference/permissions',
    'reference/feature-matrix',
    'reference/glossary'
  ]
}

module.exports = sidebars
