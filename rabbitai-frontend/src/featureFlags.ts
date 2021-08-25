import { FeatureFlagMap, FeatureFlag } from '@rabbitai-ui/core';

export { FeatureFlagMap, FeatureFlag } from '@rabbitai-ui/core';

/**
 * 初始化为指定功能。
 *
 * @param featureFlags
 */
export function initFeatureFlags(featureFlags: FeatureFlagMap) {
  if (!window.featureFlags) {
    window.featureFlags = featureFlags || {};
  }
}

/**
 * 是否已启用指定功能。
 *
 * @param feature
 */
export function isFeatureEnabled(feature: FeatureFlag) {
  return window && window.featureFlags && !!window.featureFlags[feature];
}
