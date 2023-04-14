import { restRequest } from "@girder/core/rest";

export function importDicomRT(model) {
  restRequest({
    type: "GET",
    url: `item/${model.id}/files?limit=0`,
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

export function exportDicomRT(model) {
  restRequest({
    type: "GET",
    url: `item/${model.id}/files?limit=0`,
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
