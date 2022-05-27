require.config({paths: {vs: 'https://unpkg.com/monaco-editor@0.21.2/min/vs'}});
window.MonacoEnvironment = {
  getWorkerUrl: () => proxy
};

const proxy = URL.createObjectURL(new Blob(
    [
      `
  	self.MonacoEnvironment = { baseUrl: 'https://unpkg.com/monaco-editor@0.21.2/min/' };
  	importScripts('https://unpkg.com/monaco-editor@0.21.2/min/vs/base/worker/workerMain.js');`,
    ],
    {type: 'text/javascript'}));

const $ = document.querySelector.bind(document);

require(['vs/editor/editor.main'], function() {
  editor = monaco.editor.create($('#playground'), {
    value: LANGUAGE_BUFFERS[DEFAULT_LANGUAGE],
    language: DEFAULT_LANGUAGE,
    theme: 'vs-dark',
    fontSize: '15px',
    padding: {top: '20px'},
  });
});

const ansi = new AnsiUp();
ansi.use_classes = true;

const ExecutionResult = {
  loading: () => {
    return {loading: true};
  },
  success: (exitCode, stdout, stderr) => {
    return {success: true, exitCode, stdout, stderr};
  },
  failure: () => {
    return {failure: true};
  },
};

Vue.component('results', {
  props: ['result'],
  template: `
      <div v-if="result.loading">
        <h2><span>Loading</span><span class="AnimatedEllipsis"></span></h2>
      </div>
      <div v-else>
        <div v-if="result.success">
          <h2>exit code</h2>
          <pre>{{ result.exitCode }}</pre>
          <h2>stdout</h2>
          <component :is="stdoutHtml"></component>
          <h2>stderr</h2>
          <component :is="stderrHtml"></component>
        </div>
        <div v-else>
          <h2>Loading Error</h2>
          Please try again.
        </div>
      </div>
    `,
  computed: {
    stdoutHtml() {
      const stdout = ansi.ansi_to_html(this.result.stdout);
      return {
        template: `<pre class="inner">${stdout}</pre>`,
      };
    },
    stderrHtml() {
      const stderr = ansi.ansi_to_html(this.result.stderr);
      return {
        template: `<pre class="inner">${stderr}</pre>`,
      };
    },
  },
});

const DescriptionResult = {
  loading: () => {
    return {loading: true};
  },
  success: (languageDescription, osVersion, packages) => {
    return {success: true, languageDescription, osVersion, packages};
  },
  failure: () => {
    return {failure: true};
  },
};

Vue.component('description', {
  props: ['result'],
  template: `
      <div v-if="result.loading">
        <span>Loading</span><span class="AnimatedEllipsis"></span>
      </div>
      <div v-else>
        <div v-if="result.success">
          <b>{{ result.languageDescription }} - {{ result.osVersion }}</b>
          <pre class="mb-0">{{ result.packages.join('\\n') }}</pre>
        </div>
        <div v-else>
          <h2>Loading Error</h2>
          Please try again.
        </div>
      </div>
    `,
});

const CopyStatus = {
  loading: () => {
    return {loading: true};
  },
  unsaved: () => {
    return {unsaved: true};
  },
  success: (playgroundId) => {
    return {success: true, playgroundId};
  },
  failure: () => {
    return {failure: true};
  },
};

Vue.component('copypg', {
  props: ['status', 'onClick'],
  template: `
    <div v-if="status.loading">
      <span class="AnimatedEllipsis"></span>
    </div>
    <div v-else>
      <div v-if="status.unsaved">
        <button class="btn" type="button" aria-label="Copy to clipboard" v-on:click="copyPg">
          <svg class="octicon octicon-clippy" viewBox="0 0 14 16" version="1.1" width="14" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M2 13h4v1H2v-1zm5-6H2v1h5V7zm2 3V8l-3 3 3 3v-2h5v-2H9zM4.5 9H2v1h2.5V9zM2 12h2.5v-1H2v1zm9 1h1v2c-.02.28-.11.52-.3.7-.19.18-.42.28-.7.3H1c-.55 0-1-.45-1-1V4c0-.55.45-1 1-1h3c0-1.11.89-2 2-2 1.11 0 2 .89 2 2h3c.55 0 1 .45 1 1v5h-1V6H1v9h10v-2zM2 5h8c0-.55-.45-1-1-1H8c-.55 0-1-.45-1-1s-.45-1-1-1-1 .45-1 1-.45 1-1 1H3c-.55 0-1 .45-1 1z"></path></svg>
        </button>
      </div>
      <div v-else>
        <div v-if="status.success">
          <button disabled class="btn btn-primary">
            <svg width="12" height="16" viewBox="0 0 12 16" class="octicon octicon-check" aria-hidden="true">
              <path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5L12 5z" />
            </svg>
            /{{ status.playgroundId }}
          </button>
        </div>
        <div v-else>
          <button disabled class="btn btn-danger">
            <svg width="14" height="16" viewBox="0 0 14 16" class="octicon octicon-stop" aria-hidden="true">
              <path
                fill-rule="evenodd"
                d="M10 1H4L0 5v6l4 4h6l4-4V5l-4-4zm3 9.5L9.5 14h-5L1 10.5v-5L4.5 2h5L13 5.5v5zM6 4h2v5H6V4zm0 6h2v2H6v-2z"
              />
            </svg>
            Failed
          </button>
        </div>
      </div>
    </div>
  `,
  methods: {
    copyPg() {
      this.onClick();
    },
  },
});

new Vue({
  el: '#app',
  data: {
    language: DEFAULT_LANGUAGE,
    lastLanguage: DEFAULT_LANGUAGE,
    languageOptions: Object.keys(LANGUAGE_BUFFERS),
    executionResult: DEFAULT_EXECUTION_RESULT,
    descriptionResult: DescriptionResult.success('', '', []),
    copyStatus: CopyStatus.unsaved(),
  },
  methods: {
    async run() {
      this.executionResult = ExecutionResult.loading();
      await axios
          .post('/api/rce', {
            lang: this.language,
            code: editor.getValue(),
          })
          .then((result) => {
            const {
              data: {exitcode, stdout, stderr},
            } = result;
            this.executionResult =
                ExecutionResult.success(exitcode, stdout, stderr);
          })
          .catch((e) => {
            console.error(e);
            this.executionResult = ExecutionResult.failure();
          });
    },

    async getDescription() {
      this.descriptionResult = DescriptionResult.loading();
      await axios.get(`/api/describe/${this.language}`)
          .then((result) => {
            const {
              data: {description, ubuntu, packages},
            } = result;
            this.descriptionResult = DescriptionResult.success(
                description, `Ubuntu ${ubuntu}`, packages);
          })
          .catch((e) => {
            console.error(e);
            this.descriptionResult = DescriptionResult.failure();
          });
    },

    async copyPlayground() {
      this.copyStatus = CopyStatus.loading();
      LANGUAGE_BUFFERS[this.lastLanguage] = editor.getValue();
      await axios
          .post(`api/save_playground`, {
            active_lang: this.language,
            lang_buffers: LANGUAGE_BUFFERS,
            execution_result: this.executionResult,
          })
          .then((result) => {
            const {data: {playgroundId}} = result;
            copyToClipboard(`${window.location.href}${playgroundId}`);
            this.copyStatus = CopyStatus.success(playgroundId);
          })
          .catch((e) => {
            console.error(e);
            this.copyStatus = CopyStatus.failure();
          });

      setTimeout(() => {
        this.copyStatus = CopyStatus.unsaved();
      }, 2000);
    },

    changeLanguage() {
      LANGUAGE_BUFFERS[this.lastLanguage] = editor.getValue();
      editor.setValue(LANGUAGE_BUFFERS[this.language]);
      monaco.editor.setModelLanguage(editor.getModel(), this.language);
      this.lastLanguage = this.language;
    },
  },
});

// https://stackoverflow.com/a/33928558
function copyToClipboard(text) {
  if (window.clipboardData && window.clipboardData.setData) {
    return clipboardData.setData('Text', text);
  } else if (
      document.queryCommandSupported &&
      document.queryCommandSupported('copy')) {
    var textarea = document.createElement('textarea');
    textarea.textContent = text;
    textarea.style.position =
        'fixed';  // Prevent scrolling to bottom of page in Microsoft Edge.
    document.body.appendChild(textarea);
    textarea.select();
    try {
      return document.execCommand(
          'copy');  // Security exception may be thrown by some browsers.
    } catch (ex) {
      console.warn('Copy to clipboard failed.', ex);
      return false;
    } finally {
      document.body.removeChild(textarea);
    }
  }
}
