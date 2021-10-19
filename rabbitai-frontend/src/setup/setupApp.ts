/* eslint global-require: 0 */
import $ from 'jquery';
import { SupersetClient } from '@superset-ui/core';
import {
  getClientErrorObject,
  ClientErrorObject,
} from 'src/utils/getClientErrorObject';
import setupErrorMessages from 'src/setup/setupErrorMessages';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
declare global {
  interface Window {
    $: any;
    jQuery: any;
  }
}

/**
 * 显示API相关信息。
 *
 * @param resp 客户端错误对象。
 */
function showApiMessage(resp: ClientErrorObject) {
  const template =
    '<div class="alert"> ' +
    '<button type="button" class="close" ' +
    'data-dismiss="alert">\xD7</button> </div>';
  const severity = resp.severity || 'info';
  $(template)
    .addClass(`alert-${severity}`)
    .append(resp.message || '')
    .appendTo($('#alert-container'));
}

/**
 * 切换捡选框。
 *
 * @param apiUrlPrefix API地址前缀。
 * @param selector 选择器。
 */
function toggleCheckbox(apiUrlPrefix: string, selector: string) {
  SupersetClient.get({
    endpoint: apiUrlPrefix + ($(selector)[0] as HTMLInputElement).checked,
  })
    .then(() => undefined)
    .catch(response =>
      getClientErrorObject(response).then(parsedResp => {
        if (parsedResp && parsedResp.message) {
          showApiMessage(parsedResp);
        }
      }),
    );
}

/**
 * 设置应用，初始化Web应用，Html文档就绪后执行相关操作。
 */
export default function setupApp() {
  $(document).ready(function () {
    $(':checkbox[data-checkbox-api-prefix]').change(function (
      this: HTMLElement,
    ) {
      const $this = $(this);
      const prefix = $this.data('checkbox-api-prefix');
      const id = $this.attr('id');
      toggleCheckbox(prefix, `#${id}`);
    });

    // for language picker dropdown
    $('#language-picker a').click(function (
      ev: JQuery.ClickEvent<
        HTMLLinkElement,
        null,
        HTMLLinkElement,
        HTMLLinkElement
      >,
    ) {
      ev.preventDefault();
      SupersetClient.get({
        url: ev.currentTarget.href,
        parseMethod: null,
      }).then(() => {
        window.location.reload();
      });
    });
  });

  // A set of hacks to allow apps to run within a FAB template
  // this allows for the server side generated menus to function
  window.$ = $;
  window.jQuery = $;
  require('bootstrap');

  // setup appwide custom error messages
  setupErrorMessages();
}
