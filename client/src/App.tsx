import { useEffect, useState } from 'react'
import './App.css'
import UploadButton from './components/Upload'
import axios from 'axios'
import LevelsList from './components/LevelList'

function App() {
  const [levels, setLevels] = useState([])
  useEffect(() => {
    axios.get('http://localhost:8000/api/levels').then(res => setLevels(res.data))
  }, [])
  console.log('levels', levels)
  return (
    <>
      <h1>Hello</h1>
      <UploadButton />
      <LevelsList levels={levels} />
    </>
  )
}

export default App
