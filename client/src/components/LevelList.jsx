import React from "react";
import { Avatar, Space, Table } from "antd";
import { blue, green, red } from "@ant-design/colors";
import "../App.css";

const columns = [
  {
    title: "File Name",
    dataIndex: "filename",
    key: "filname",
    width: "10%",
  },
  {
    title: "Matrix",
    dataIndex: "matrix",
    key: "matrix",
    width: "25%",
    render: (matrix) => (
      <Space direction="vertical" size={2}>
        {matrix
          ? matrix.map((row, index) => (
              <Space key={index} wrap size={2}>
                {row.map((letter, index) => (
                  <Avatar
                    style={{ backgroundColor: blue[3] }}
                    key={index}
                    shape="square"
                  >
                    {letter}
                  </Avatar>
                ))}
              </Space>
            ))
          : null}
      </Space>
    ),
  },
  {
    title: "Words",
    dataIndex: "words",
    key: "words",
    width: "25%",
    render: (words) => <div>{words ? words.join(", ") : null}</div>,
  },
  {
    title: "Bonus",
    dataIndex: "bonus_words",
    key: "bonus_words",
    width: "25%",
    render: (bonus) => <div>{bonus ? bonus.join(", ") : null}</div>,
  },
  {
    title: "Status",
    dataIndex: "status",
    key: "status",
    width: "15%",
    render: (status) => (
      <div
        style={{
          color: status === "valid" ? green.primary : red.primary,
        }}
      >
        <b>{status}</b>
      </div>
    ),
  },
];

const LevelsList = ({ levels, total, onChange }) => (
  <div className="table-wrapper">
    <Table
      onChange={onChange}
      pagination={{ pageSize: 20, total: total }}
      columns={columns}
      dataSource={levels}
    />
  </div>
);

export default LevelsList;
