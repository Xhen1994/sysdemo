import React, { useState, useEffect } from 'react'
import { Table, Button, Card, Tag, message } from 'antd'
import { PlusOutlined } from '@ant-design/icons'
import api from '../services/api'

const ProjectList: React.FC = () => {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadProjects()
  }, [])

  const loadProjects = async () => {
    setLoading(true)
    try {
      const response = await api.get('/projects')
      setProjects(response.data)
    } catch (error) {
      message.error('加载失败')
    } finally {
      setLoading(false)
    }
  }

  const statusColors: Record<string, string> = {
    planning: 'blue',
    in_progress: 'orange',
    on_hold: 'default',
    completed: 'green',
    cancelled: 'red'
  }

  const statusLabels: Record<string, string> = {
    planning: '规划中',
    in_progress: '进行中',
    on_hold: '暂停',
    completed: '已完成',
    cancelled: '已取消'
  }

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 60,
    },
    {
      title: '项目名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '项目代码',
      dataIndex: 'code',
      key: 'code',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={statusColors[status]}>
          {statusLabels[status]}
        </Tag>
      ),
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
    },
    {
      title: '项目经理',
      dataIndex: 'manager_name',
      key: 'manager_name',
    },
    {
      title: '经理联系方式',
      dataIndex: 'manager_contact',
      key: 'manager_contact',
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => new Date(date).toLocaleDateString('zh-CN'),
    },
  ]

  return (
    <div>
      <Card>
        <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
          <h1>项目管理</h1>
          <Button type="primary" icon={<PlusOutlined />} disabled>
            新建项目（需要管理员权限）
          </Button>
        </div>

        <Table
          columns={columns}
          dataSource={projects}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 20,
            showTotal: (total) => `共 ${total} 条`,
          }}
        />
      </Card>
    </div>
  )
}

export default ProjectList



