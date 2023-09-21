// import { UploadOutlined } from "@ant-design/icons";
import { Button, message, Modal, Form, Input } from "antd";
import { createLevels } from "../utils/api";

// const UploadButton = ({ onSuccessLoad }) => (
//   <Upload
//     name="file"
//     action="http://localhost:8000/api/levels"
//     onChange={(info) => {
//       console.log("info", info);
//       if (info.file.status !== "uploading") {
//         console.log(info.file, info.fileList);
//       }
//       if (info.file.status === "done") {
//         message.success(`${info.file.name} file uploaded successfully`);

//         Modal.warning({
//           title: "Some errors occured while parsing",
//           content: (
//             <div>
//               {info.file.response
//                 .filter((level) => level.status !== "valid")
//                 .map((level) => (
//                   <p>{level.filename} - {level.status}</p>
//                 ))}
//             </div>
//           ),
//           onOk() {},
//         });

//         onSuccessLoad();
//       } else if (info.file.status === "error") {
//         message.error(`${info.file.name} file upload failed.`);
//       }
//     }}
//     maxCount={1}
//   >
//     <Button icon={<UploadOutlined />}>Click to Upload</Button>
//   </Upload>
// );

// export default UploadButton;

const LoadForm = ({onSuccessLoad}) => {
  const onFinish = (values) => {
    createLevels(values).then((levels) => {
      Modal.warning({
        title: "Some errors occured while parsing",
        content: (
          <div>
            {levels.map((level) => (
              <p>
                {level.filename} - {level.status}
              </p>
            ))}
          </div>
        ),
        onOk() {},
      });

      onSuccessLoad();
    }).catch(() => message.error('Cannot download url'));
  };

  const onFinishFailed = (errorInfo) => {
    message.error("Failed to load url", errorInfo);
  };

  return (
    <Form
      layout="inline"
      name="basic"
      onFinish={onFinish}
      onFinishFailed={onFinishFailed}
      autoComplete="off"
    >
      <Form.Item
        label="Zip URL"
        name="url"
        style={{ width: 935 }}
        rules={[
          {
            required: true,
            message: "Please input your url!",
          },
        ]}
      >
        <Input />
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit">
          Load
        </Button>
      </Form.Item>
    </Form>
  );
};
export default LoadForm;
