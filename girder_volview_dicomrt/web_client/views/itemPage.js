import { wrap } from "@girder/core/utilities/PluginUtils";
import ItemView from "@girder/core/views/body/ItemView";
import { importDicomRT, exportDicomRT } from "./dicomRT";

wrap(ItemView, "render", function (render) {
  this.once("g:rendered", function () {
    this.$el.find(".g-item-header .btn-group").before(
      `
      <a class="btn btn-sm btn-primary export-dicomrt" style="margin-left: 10px" role="button">
        <i class="icon-link-ext"></i>Export DICOM-RT
      </a>
      <a class="btn btn-sm btn-primary import-dicomrt" style="margin-left: 10px" role="button">
        <i class="icon-link-ext"></i>Import DICOM-RT
      </a>
      `
    );
    this.$el.find(".export-dicomrt")[0].onclick = () => exportDicomRT(this.model);
    this.$el.find(".import-dicomrt")[0].onclick = () => importDicomRT(this.model);
  });
  render.call(this);
});
