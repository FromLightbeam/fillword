import { UploadOutlined } from "@ant-design/icons";
import { Button, message, Upload } from "antd";

const UploadButton = ({onSuccessLoad}) => (
  <Upload
    name="file"
    action="http://localhost:8000/api/levels"
    onChange={(info) => {
      console.log("info", info);
      if (info.file.status !== "uploading") {
        console.log(info.file, info.fileList);
      }
      if (info.file.status === "done") {
        message.success(`${info.file.name} file uploaded successfully`);
        onSuccessLoad()
      } else if (info.file.status === "error") {
        message.error(`${info.file.name} file upload failed.`);
      }
    }}
    maxCount={1}
  >
    <Button icon={<UploadOutlined />}>Click to Upload</Button>
  </Upload>
);

export default UploadButton;
