
import sinon from 'sinon';
import { SupersetClient } from '@rabbitai-ui/core';
import logger from 'src/middleware/loggerMiddleware';
import { LOG_EVENT } from 'src/logger/actions';
import { LOG_ACTIONS_LOAD_CHART } from 'src/logger/LogUtils';

describe('logger middleware', () => {
  const next = sinon.spy();
  const mockStore = {
    getState: () => ({
      dashboardInfo: {
        id: 1,
      },
      impressionId: 'impression_id',
    }),
  };
  const action = {
    type: LOG_EVENT,
    payload: {
      eventName: LOG_ACTIONS_LOAD_CHART,
      eventData: {
        key: 'value',
        start_offset: 100,
      },
    },
  };

  let postStub;
  beforeEach(() => {
    postStub = sinon.stub(SupersetClient, 'post');
  });
  afterEach(() => {
    next.resetHistory();
    postStub.restore();
  });

  it('should listen to LOG_EVENT action type', () => {
    const action1 = {
      type: 'ACTION_TYPE',
      payload: {
        some: 'data',
      },
    };
    logger(mockStore)(next)(action1);
    expect(next.callCount).toBe(1);
  });

  it('should POST an event to /rabbitai/log/ when called', () => {
    const clock = sinon.useFakeTimers();
    logger(mockStore)(next)(action);
    expect(next.callCount).toBe(0);

    clock.tick(2000);
    expect(SupersetClient.post.callCount).toBe(1);
    expect(SupersetClient.post.getCall(0).args[0].endpoint).toMatch(
      '/rabbitai/log/',
    );
  });

  it('should include ts, start_offset, event_name, impression_id, source, and source_id in every event', () => {
    const clock = sinon.useFakeTimers();
    logger(mockStore)(next)(action);
    clock.tick(2000);

    expect(SupersetClient.post.callCount).toBe(1);
    const { events } = SupersetClient.post.getCall(0).args[0].postPayload;
    const mockEventdata = action.payload.eventData;
    const mockEventname = action.payload.eventName;
    expect(events[0]).toMatchObject({
      key: mockEventdata.key,
      event_name: mockEventname,
      impression_id: mockStore.getState().impressionId,
      source: 'dashboard',
      source_id: mockStore.getState().dashboardInfo.id,
      event_type: 'timing',
    });

    expect(typeof events[0].ts).toBe('number');
    expect(typeof events[0].start_offset).toBe('number');
  });

  it('should debounce a few log requests to one', () => {
    const clock = sinon.useFakeTimers();
    logger(mockStore)(next)(action);
    logger(mockStore)(next)(action);
    logger(mockStore)(next)(action);
    clock.tick(2000);

    expect(SupersetClient.post.callCount).toBe(1);
    expect(
      SupersetClient.post.getCall(0).args[0].postPayload.events,
    ).toHaveLength(3);
  });
});
