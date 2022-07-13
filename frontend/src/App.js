import { Navigate, Route, Routes } from 'react-router-dom'
import SearchPage from './pages/SearchPage'

function App() {
  return (
    <Routes>
      <Route path="/hsource" element={<SearchPage />} />
      <Route path="*" element={<Navigate to="hsource" />} />
    </Routes>
  );
}

export default App;
