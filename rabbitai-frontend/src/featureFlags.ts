import { FeatureFlagMap, FeatureFlag } from '@superset-ui/core';

export { FeatureFlagMap, FeatureFlag } from '@superset-ui/core';

/**
 * 初始化为指定特性标志，即设置：window.featureFlags = featureFlags。
 *
 * @param featureFlags 特性标志。
 */
export function initFeatureFlags(featureFlags: FeatureFlagMap) {
  if (!window.featureFlags) {
    window.featureFlags = featureFlags || {};
  }
}

/**
 * 判断当前应用程序是否具有指定特性标志。
 *
 * @param feature 特性标志。
 */
export function isFeatureEnabled(feature: FeatureFlag) {
  return window && window.featureFlags && !!window.featureFlags[feature];
}
