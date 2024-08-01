import { wrap } from "@girder/core/utilities/PluginUtils";
import ItemView from "@girder/core/views/body/ItemView";
import { importDicomRT, exportDicomRT } from "./dicomRT";
import { restRequest } from "@girder/core/rest";

wrap(ItemView, "render", function (render) {
  this.once("g:rendered", function () {
    // check if item has loadable files
    const id = this.model.id;
    restRequest({
      url: `item/${id}/volview_loadable`,
      method: "GET",
      error: null
    }).done((loadableJSON) => {
      if (loadableJSON.loadable) {
        this.$el.find(".g-item-header .btn-group").before(
          `
          <a class="btn btn-sm btn-primary export-dicomrt" style="margin-left: 10px" role="button" title="Assumes a session.volview.zip file exists on this item">
            Export DICOM-RT
          </a>
          <a class="btn btn-sm btn-primary import-dicomrt" style="margin-left: 10px" role="button" title="Assumes rt.dcm and session.volview.zip files exist on this item">
            Import DICOM-RT
          </a>
          `
        );
        this.$el.find(".export-dicomrt")[0].onclick = () => exportDicomRT(this.model);
        this.$el.find(".import-dicomrt")[0].onclick = () => importDicomRT(this.model);
      }
    });
  });
  render.call(this);
});
