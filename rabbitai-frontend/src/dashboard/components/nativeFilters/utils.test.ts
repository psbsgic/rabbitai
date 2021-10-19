import { Behavior, FeatureFlag } from '@superset-ui/core';
import * as featureFlags from 'src/featureFlags';
import { nativeFilterGate } from './utils';

let isFeatureEnabledMock: jest.MockInstance<boolean, [feature: FeatureFlag]>;

describe('nativeFilterGate', () => {
  describe('with all feature flags disabled', () => {
    beforeAll(() => {
      isFeatureEnabledMock = jest
        .spyOn(featureFlags, 'isFeatureEnabled')
        .mockImplementation(() => false);
    });

    afterAll(() => {
      // @ts-ignore
      isFeatureEnabledMock.restore();
    });

    it('should return true for regular chart', () => {
      expect(nativeFilterGate([])).toEqual(true);
    });

    it('should return true for cross filter chart', () => {
      expect(nativeFilterGate([Behavior.INTERACTIVE_CHART])).toEqual(true);
    });

    it('should return false for native filter chart with cross filter support', () => {
      expect(
        nativeFilterGate([Behavior.NATIVE_FILTER, Behavior.INTERACTIVE_CHART]),
      ).toEqual(false);
    });

    it('should return false for native filter behavior', () => {
      expect(nativeFilterGate([Behavior.NATIVE_FILTER])).toEqual(false);
    });
  });

  describe('with only native filters feature flag enabled', () => {
    beforeAll(() => {
      isFeatureEnabledMock = jest
        .spyOn(featureFlags, 'isFeatureEnabled')
        .mockImplementation(
          (featureFlag: FeatureFlag) =>
            featureFlag === FeatureFlag.DASHBOARD_NATIVE_FILTERS,
        );
    });

    afterAll(() => {
      // @ts-ignore
      isFeatureEnabledMock.restore();
    });

    it('should return true for regular chart', () => {
      expect(nativeFilterGate([])).toEqual(true);
    });

    it('should return true for cross filter chart', () => {
      expect(nativeFilterGate([Behavior.INTERACTIVE_CHART])).toEqual(true);
    });

    it('should return false for native filter chart with cross filter support', () => {
      expect(
        nativeFilterGate([Behavior.NATIVE_FILTER, Behavior.INTERACTIVE_CHART]),
      ).toEqual(false);
    });

    it('should return false for native filter behavior', () => {
      expect(nativeFilterGate([Behavior.NATIVE_FILTER])).toEqual(false);
    });
  });

  describe('with native filters and experimental feature flag enabled', () => {
    beforeAll(() => {
      isFeatureEnabledMock = jest
        .spyOn(featureFlags, 'isFeatureEnabled')
        .mockImplementation((featureFlag: FeatureFlag) =>
          [
            FeatureFlag.DASHBOARD_CROSS_FILTERS,
            FeatureFlag.DASHBOARD_FILTERS_EXPERIMENTAL,
          ].includes(featureFlag),
        );
    });

    afterAll(() => {
      // @ts-ignore
      isFeatureEnabledMock.restore();
    });

    it('should return true for regular chart', () => {
      expect(nativeFilterGate([])).toEqual(true);
    });

    it('should return true for cross filter chart', () => {
      expect(nativeFilterGate([Behavior.INTERACTIVE_CHART])).toEqual(true);
    });

    it('should return true for native filter chart with cross filter support', () => {
      expect(
        nativeFilterGate([Behavior.NATIVE_FILTER, Behavior.INTERACTIVE_CHART]),
      ).toEqual(true);
    });

    it('should return false for native filter behavior', () => {
      expect(nativeFilterGate([Behavior.NATIVE_FILTER])).toEqual(false);
    });
  });
});
