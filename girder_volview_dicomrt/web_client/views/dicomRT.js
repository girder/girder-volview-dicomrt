import { restRequest } from "@girder/core/rest";

function run(item, operation) {
  restRequest({
    type: "POST",
    url: `/slicer_cli_web/ghcr.io_girder_girder-volview-dicomrt_worker-volview-dicomrt_latest/volview_dicomrt/run`,
    data: {
      operation,
      item,
      girderApiUrl: '',
      girderToken: '',
    },
    error: null,
  })
    .done((resp) => {
      console.log("done");
    })
    .fail((resp) => {
      events.trigger("g:alert", {
        icon: "cancel",
        text: "Could not check files to open in VolView",
        type: "danger",
        timeout: 4000,
      });
    });
}

export function importDicomRT(model) {
  run(model.id, "import");
}

export function exportDicomRT(model) {
  run(model.id, "export");
}
