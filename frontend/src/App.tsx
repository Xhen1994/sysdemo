import React, { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Layout, message } from 'antd'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import IssueList from './pages/IssueList'
import IssueDetail from './pages/IssueDetail'
import IssueCreate from './pages/IssueCreate'
import DepartmentList from './pages/DepartmentList'
import ProjectList from './pages/ProjectList'
import AIAnalysis from './pages/AIAnalysis'
import AppLayout from './components/Layout/AppLayout'
import { AuthProvider, useAuth } from './context/AuthContext'

const { Content } = Layout

// 受保护的路由组件
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth()
  
  if (!isAuthenticated) {
    message.warning('请先登录')
    return <Navigate to="/login" replace />
  }
  
  return <>{children}</>
}

const AppRoutes: React.FC = () => {
  const { isAuthenticated } = useAuth()

  return (
    <Routes>
      <Route path="/login" element={isAuthenticated ? <Navigate to="/" /> : <Login />} />
      
      <Route path="/" element={
        <ProtectedRoute>
          <AppLayout />
        </ProtectedRoute>
      }>
        <Route index element={<Dashboard />} />
        <Route path="issues" element={<IssueList />} />
        <Route path="issues/create" element={<IssueCreate />} />
        <Route path="issues/:id" element={<IssueDetail />} />
        <Route path="departments" element={<DepartmentList />} />
        <Route path="projects" element={<ProjectList />} />
        <Route path="ai-analysis" element={<AIAnalysis />} />
      </Route>
      
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App



