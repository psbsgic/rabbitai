import { SyntheticEvent } from 'react';
import domToImage, { Options } from 'dom-to-image';
import kebabCase from 'lodash/kebabCase';
import { t } from '@superset-ui/core';
import { addWarningToast } from 'src/messageToasts/actions';

/**
 * @remark
 * same as https://github.com/apache/rabbitai/blob/c53bc4ddf9808a8bb6916bbe3cb31935d33a2420/rabbitai-frontend/stylesheets/less/variables.less#L34
 */
const GRAY_BACKGROUND_COLOR = '#F5F5F5';

/**
 * generate a consistent file stem from a description and date
 *
 * @param description title or description of content of file
 * @param date date when file was generated
 */
const generateFileStem = (description: string, date = new Date()) =>
  `${kebabCase(description)}-${date.toISOString().replace(/[: ]/g, '-')}`;

/**
 * Create an event handler for turning an element into an image
 *
 * @param selector css selector of the parent element which should be turned into image
 * @param description name or a short description of what is being printed.
 *   Value will be normalized, and a date as well as a file extension will be added.
 * @param domToImageOptions dom-to-image Options object.
 * @param isExactSelector if false, searches for the closest ancestor that matches selector.
 * @returns event handler
 */
export default function downloadAsImage(
  selector: string,
  description: string,
  domToImageOptions: Options = {},
  isExactSelector = false,
) {
  return (event: SyntheticEvent) => {
    const elementToPrint = isExactSelector
      ? document.querySelector(selector)
      : event.currentTarget.closest(selector);

    if (!elementToPrint) {
      return addWarningToast(
        t('Image download failed, please refresh and try again.'),
      );
    }

    // Mapbox controls are loaded from different origin, causing CORS error
    // See https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toDataURL#exceptions
    const filter = (node: Element) => {
      if (typeof node.className === 'string') {
        return (
          node.className !== 'mapboxgl-control-container' &&
          !node.className.includes('ant-dropdown')
        );
      }
      return true;
    };

    return domToImage
      .toJpeg(elementToPrint, {
        quality: 0.95,
        bgcolor: GRAY_BACKGROUND_COLOR,
        filter,
      })
      .then(dataUrl => {
        const link = document.createElement('a');
        link.download = `${generateFileStem(description)}.jpg`;
        link.href = dataUrl;
        link.click();
      })
      .catch(e => {
        console.error('Creating image failed', e);
      });
  };
}
