import React from "react";
import { Avatar, Row, Space, Table } from "antd";
import type { ColumnsType } from "antd/es/table";

interface DataType {
  key: string;
  name: string;
  age: number;
  address: string;
  tags: string[];
}

const columns: ColumnsType<DataType> = [
  {
    title: "Matrix",
    dataIndex: "matrix",
    key: "matrix",
    render: (matrix) => (
      <Space direction="vertical" size={2}>
        {matrix.map((row) => (
          <Space wrap size={2}>
            {row.map((letter) => (
              <Avatar shape="square">{letter}</Avatar>
            ))}
          </Space>
        ))}
      </Space>
    ),
  },
  {
    title: "Words",
    dataIndex: "words",
    key: "words",
    render: (words) => (<div>{words.join(', ')}</div>)
  },
  {
    title: "Bonus",
    dataIndex: "bonus",
    key: "bonus",
    render: (bonus) => (<div>{bonus.join(', ')}</div>)
  },
];

const LevelsList: React.FC = ({ levels }) => (
  <Table columns={columns} dataSource={levels} />
);

export default LevelsList;
