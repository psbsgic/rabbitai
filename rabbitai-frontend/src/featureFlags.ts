import { FeatureFlagMap, FeatureFlag } from '@rabbitai-ui/core';

export { FeatureFlagMap, FeatureFlag } from '@rabbitai-ui/core';

export function initFeatureFlags(featureFlags: FeatureFlagMap) {
  if (!window.featureFlags) {
    window.featureFlags = featureFlags || {};
  }
}

export function isFeatureEnabled(feature: FeatureFlag) {
  return window && window.featureFlags && !!window.featureFlags[feature];
}
