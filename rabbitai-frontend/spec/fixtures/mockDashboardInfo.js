
export default {
  id: 1234,
  slug: 'dashboardSlug',
  metadata: {
    native_filter_configuration: [
      {
        id: 'DefaultsID',
        filterType: 'filter_select',
        targets: [{}],
        cascadeParentIds: [],
      },
    ],
  },
  userId: 'mock_user_id',
  dash_edit_perm: true,
  dash_save_perm: true,
  common: {
    flash_messages: [],
    conf: { ENABLE_JAVASCRIPT_CONTROLS: false, RABBITAI_WEBSERVER_TIMEOUT: 60 },
  },
};
