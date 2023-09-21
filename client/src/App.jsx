import { useEffect, useState } from "react";
import "./App.css";
import UploadButton from "./components/Upload";

import LevelsList from "./components/LevelList";
import { Button, Card, Progress, Space, Spin } from "antd";
import { findBonuses, getLevels } from "./utils/api";

function App() {
  const [levelData, setLevels] = useState({ levels: [], total_count: 0 });
  const [progress, setProgress] = useState(0);
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    setLoading(true);
    getLevels()
      .then((levels) => setLevels(levels))
      .finally(() => setLoading(false));
  }, []);

  const handleFindBonuses = () => {
    setLoading(true);
    findBonuses(setProgress, levelData.total_count)
      .then(() => getLevels().then((levels) => setLevels(levels)))
      .finally(() => setLoading(false));
  };

  return (
    <Space direction="vertical">
      <h1>Fillword Viewer</h1>
      <Space direction="vertical" size={16}>
        <Card>
          <UploadButton
            onSuccessLoad={() =>
              getLevels().then((levels) => setLevels(levels))
            }
          />
        </Card>

        {levelData.levels.length ? (
          <Card>
            <Progress percent={progress} />

            <Button
              disabled={!levelData.levels.length}
              type="primary"
              onClick={handleFindBonuses}
            >
              Find bonus words
            </Button>
          </Card>
        ) : null}
      </Space>
      <Spin tip="Loading" spinning={loading}>
        <LevelsList
          onChange={(pagination) => {
            getLevels({
              limit: pagination.pageSize,
              offset: (pagination.current - 1) * pagination.pageSize,
            }).then((levels) => setLevels(levels));
          }}
          levels={levelData.levels}
          total={levelData.total_count}
        />
      </Spin>
    </Space>
  );
}

export default App;
