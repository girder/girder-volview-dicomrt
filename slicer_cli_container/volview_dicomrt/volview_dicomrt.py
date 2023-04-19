import pprint
from progress_helper import ProgressHelper
import shutil
from ctk_cli import CLIArgumentParser
import sys
import os
import glob
import zipfile


def vti_to_rt(series_path, vti_file, rt_file):
    import vtk
    import numpy as np
    from rt_utils import RTStructBuilder
    rtstruct = RTStructBuilder.create_new(dicom_series_path=series_path)
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(vti_file)
    reader.Update()
    dims = reader.GetOutput().GetDimensions()
    scalar_data = reader.GetOutput().GetPointData().GetScalars()

    # Restructure .vti file scalar array into rt_utils format
    arr = np.array(scalar_data, dtype=bool).reshape(dims, order='F').swapaxes(0, 1)

    rtstruct.add_roi(mask=arr)
    rtstruct.save(rt_file)


def rt_to_vti(series_path, rt_file, vti_file):
    import itk
    import vtk
    import numpy as np
    from rt_utils import RTStructBuilder
    rtstruct = RTStructBuilder.create_from(dicom_series_path=series_path, rt_struct_path=rt_file)
    names = rtstruct.get_roi_names()

    # Restructure rt_utils format into .vti file scalar array
    arr = rtstruct.get_roi_mask_by_name(names[0]).astype(np.float32).transpose(2,0,1).copy()

    labelmap = itk.GetImageFromArray(arr)

    # Get the spacing, etc. from the DICOM series
    image = itk.imread(series_path, itk.F)
    labelmap.CopyInformation(image)

    vtk_image = itk.vtk_image_from_image(labelmap)
    writer = vtk.vtkXMLImageDataWriter()
    writer.SetFileName(vti_file)
    writer.SetInputData(vtk_image)
    writer.Write()

def main(args):
    print('>> parsed arguments')
    import girder_client
    pprint.pprint(vars(args))
    with ProgressHelper('DICOM-RT ' + args.operation, 'Initializing girder client ...') as p:
        step = 0
        steps = 9
        p.progress(step/steps)
        step += 1
        gc = girder_client.GirderClient(apiUrl=args.girderApiUrl)
        gc.setToken(args.girderToken)

        p.message('Creating temp directory ...')
        p.progress(step/steps)
        step += 1
        try:
            shutil.rmtree('temp')
        except:
            pass
        os.mkdir("temp")

        p.message('Downloading item ...')
        p.progress(step/steps)
        step += 1
        gc.downloadItem(args.item, "temp")

        item_path = os.path.join("temp", os.listdir("temp")[0])
        session_file = os.path.join(item_path, "session.volview.zip")

        p.message('Unzipping item files ...')
        p.progress(step/steps)
        step += 1
        for zipped_file in glob.glob(os.path.join(item_path, '*.zip')):
            p.message('Unzipping ' + zipped_file)
            with zipfile.ZipFile(zipped_file, 'r') as zip_ref:
                zip_ref.extractall(item_path)

        # Find the DICOM series directory
        p.message('Finding the DICOM series directory ...')
        p.progress(step/steps)
        step += 1
        dicom_files = list(f for f in glob.glob(os.path.join(item_path, "**"), recursive=True) if os.path.isfile(f) and f.split('.')[-1] in ['dcm', 'DCM', 'dicom', 'DICOM'] and not f.endswith('/rt.dcm'))
        if (len(dicom_files) == 0):
            raise("No DICOM series found")
        series_path = os.path.dirname(dicom_files[0])

        # Extract VolView session file
        p.message('Extracting VolView session ...')
        p.progress(step/steps)
        step += 1
        with zipfile.ZipFile(session_file, 'r') as zip_ref:
            zip_ref.extractall(os.path.join("temp", "session"))

        vti_file = os.path.join("temp", "session", "labels", "2.vti")
        rt_file = os.path.join(item_path, "rt.dcm")

        p.message('Finding relevant item files for import and export ...')
        p.progress(step/steps)
        step += 1
        girder_session_file = None
        girder_rt_file = None
        for item_file in gc.listFile(args.item):
            if item_file['name'] == "rt.dcm":
                girder_rt_file = item_file
            elif item_file['name'] == "session.volview.zip":
                girder_session_file = item_file

        if (args.operation == "export"):
            p.message("Exporting to DICOM-RT ...")
            p.progress(step/steps)
            step += 1
            vti_to_rt(series_path, vti_file, rt_file)
            p.message("Uploading result ...")
            p.progress(step/steps)
            step += 1
            rt_size = os.path.getsize(rt_file)
            with open(rt_file, mode='rb') as rt_data:
                if girder_rt_file is None:
                    gc.uploadFile(args.item, rt_data, "rt.dcm", rt_size)
                else:
                    gc.uploadFileContents(girder_rt_file['_id'], rt_data, rt_size)
        elif (args.operation == "import"):
            p.message("Importing from DICOM-RT ...")
            p.progress(step/steps)
            step += 1
            rt_to_vti(series_path, rt_file, vti_file)
            p.message("Uploading result ...")
            p.progress(step/steps)
            step += 1
            shutil.make_archive(session_file, 'zip', os.path.join('temp', 'session'))
            session_size = os.path.getsize(session_file)
            with open(session_file, mode='rb') as session_data:
                if girder_session_file is None:
                    gc.uploadFile(args.item, session_data, "session.volview.zip", session_size)
                else:
                    gc.uploadFileContents(girder_session_file['_id'], session_data, session_size)
        p.progress(1)



if __name__ == '__main__':
    main(CLIArgumentParser().parse_args())
