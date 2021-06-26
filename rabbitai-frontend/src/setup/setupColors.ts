import airbnb from '@rabbitai-ui/core/lib/color/colorSchemes/categorical/airbnb';
import categoricalD3 from '@rabbitai-ui/core/lib/color/colorSchemes/categorical/d3';
import echarts from '@rabbitai-ui/core/lib/color/colorSchemes/categorical/echarts';
import google from '@rabbitai-ui/core/lib/color/colorSchemes/categorical/google';
import lyft from '@rabbitai-ui/core/lib/color/colorSchemes/categorical/lyft';
import preset from '@rabbitai-ui/core/lib/color/colorSchemes/categorical/preset';
import sequentialCommon from '@rabbitai-ui/core/lib/color/colorSchemes/sequential/common';
import sequentialD3 from '@rabbitai-ui/core/lib/color/colorSchemes/sequential/d3';
import {
  CategoricalScheme,
  getCategoricalSchemeRegistry,
  getSequentialSchemeRegistry,
  SequentialScheme,
} from '@rabbitai-ui/core';
import rabbitai from '@rabbitai-ui/core/lib/color/colorSchemes/categorical/rabbitai';

export default function setupColors(
  extraCategoricalColorSchemas: CategoricalScheme[] = [],
  extraSequentialColorSchemes: SequentialScheme[] = [],
) {
  // Register color schemes
  const categoricalSchemeRegistry = getCategoricalSchemeRegistry();

  if (extraCategoricalColorSchemas?.length > 0) {
    extraCategoricalColorSchemas.forEach(scheme => {
      categoricalSchemeRegistry.registerValue(scheme.id, scheme);
    });
  }

  [rabbitai, airbnb, categoricalD3, echarts, google, lyft, preset].forEach(
    group => {
      group.forEach(scheme => {
        categoricalSchemeRegistry.registerValue(scheme.id, scheme);
      });
    },
  );
  categoricalSchemeRegistry.setDefaultKey('rabbitaiColors');

  const sequentialSchemeRegistry = getSequentialSchemeRegistry();

  if (extraSequentialColorSchemes?.length > 0) {
    extraSequentialColorSchemes.forEach(scheme => {
      categoricalSchemeRegistry.registerValue(scheme.id, scheme);
    });
  }

  [sequentialCommon, sequentialD3].forEach(group => {
    group.forEach(scheme => {
      sequentialSchemeRegistry.registerValue(scheme.id, scheme);
    });
  });
  sequentialSchemeRegistry.setDefaultKey('rabbitai_seq_1');
}
