import axios from "axios";

const backend = import.meta.env.VITE_BACKEND_URL

export const getLevels = ({ limit, offset } = { limit: 20, offset: 0 }) => {
  return axios
    .get(`${backend}/api/levels?limit=${limit}&offset=${offset}`)
    .then((res) => res.data);
};

export const findBonuses = (setProgress, total) => {
  // TODO: make websocket connection
  const size = 300;
  const reqNumber = total / size > 1 ? total / size : 1
  return Promise.all(
    [...Array(reqNumber).keys()].map((index) => {
      return axios
        .post(`${backend}/api/bonus`, {
          offset: index * size,
          limit: size,
        })
        .then(() => setProgress(progress => progress + (size / total) * 100));
    })
  );
};

export const createLevels = (values) => {
  return axios
    .post(`${backend}/api/levels`, values)
    .then((res) => res.data);
};
