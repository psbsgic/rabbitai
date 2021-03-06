import 'core-js/stable';
import 'regenerator-runtime/runtime';
import 'abortcontroller-polyfill/dist/abortcontroller-polyfill-only';
import 'jest-enzyme';
import jQuery from 'jquery';
import { configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { configure as configureTranslation } from '@superset-ui/core';
import { Worker } from './Worker';
import { IntersectionObserver } from './IntersectionObserver';
import setupRabbitaiClient from './setupRabbitaiClient';

configure({ adapter: new Adapter() });

const exposedProperties = ['window', 'navigator', 'document'];

const { defaultView } = document;
if (defaultView != null) {
  Object.keys(defaultView).forEach(property => {
    if (typeof global[property] === 'undefined') {
      exposedProperties.push(property);
      global[property] = defaultView[property];
    }
  });
}

const g = global as any;
g.window = g.window || {};
g.window.location = { href: 'about:blank' };
g.window.performance = { now: () => new Date().getTime() };
g.window.Worker = Worker;
g.window.IntersectionObserver = IntersectionObserver;
g.URL.createObjectURL = () => '';

Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(), // Deprecated
    removeListener: jest.fn(), // Deprecated
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

g.$ = jQuery(g.window);

configureTranslation();
setupRabbitaiClient();
