import { debounce } from 'lodash';

class DebouncedMessageQueue {
  constructor({
    callback = () => {},
    sizeThreshold = 1000,
    delayThreshold = 1000,
  }) {
    this.queue = [];
    this.sizeThreshold = sizeThreshold;
    this.delayThrehold = delayThreshold;

    this.trigger = debounce(this.trigger.bind(this), this.delayThrehold);
    this.callback = callback;
  }

  append(eventData) {
    this.queue.push(eventData);
    this.trigger();
  }

  trigger() {
    if (this.queue.length > 0) {
      const events = this.queue.splice(0, this.sizeThreshold);
      this.callback.call(null, events);

      // If there are remaining items, call it again.
      if (this.queue.length > 0) {
        this.trigger();
      }
    }
  }
}

export default DebouncedMessageQueue;
