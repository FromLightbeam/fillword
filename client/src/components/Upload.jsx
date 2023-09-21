import { Button, message, Modal, Form, Input } from "antd";
import { createLevels } from "../utils/api";

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
