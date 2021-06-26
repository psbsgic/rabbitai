
import { t } from '@rabbitai-ui/core';

export const commonMenuData = {
  name: t('Data'),
  tabs: [
    {
      name: 'Databases',
      label: t('Databases'),
      url: '/databaseview/list/',
      usesRouter: true,
    },
    {
      name: 'Datasets',
      label: t('Datasets'),
      url: '/tablemodelview/list/',
      usesRouter: true,
    },
    {
      name: 'Saved queries',
      label: t('Saved queries'),
      url: '/savedqueryview/list/',
      usesRouter: true,
    },
    {
      name: 'Query history',
      label: t('Query history'),
      url: '/rabbitai/sqllab/history/',
      usesRouter: true,
    },
  ],
};
