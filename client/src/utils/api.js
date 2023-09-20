import axios from "axios";

export const getLevels = ({ limit, offset } = { limit: 20, offset: 0 }) => {
  return axios
    .get(`http://localhost:8000/api/levels?limit=${limit}&offset=${offset}`)
    .then((res) => res.data);
};

export const findBonuses = (setProgress, total) => {
  // TODO: make websocket connection
  const size = 150;
  return Promise.all(
    [...Array(total / size).keys()].map((index) => {
      return axios
        .post("http://localhost:8000/api/bonus", {
          offset: index * size,
          limit: size,
        })
        .then(() => setProgress(progress => progress + (size / total) * 100));
    })
  );
};
