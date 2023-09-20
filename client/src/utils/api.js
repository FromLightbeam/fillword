import axios from "axios";

export const getLevels = ({limit, offset} = {limit: 20, offset: 0}) => {
  return axios
    .get(`http://localhost:8000/api/levels?limit=${limit}&offset=${offset}`)
    .then((res) => res.data);
};

export const findBonuses = () => {
  return axios
    .post("http://localhost:8000/api/bonus", { offset: 0, limit: 500 })
    .then((res) => res.data);
};
