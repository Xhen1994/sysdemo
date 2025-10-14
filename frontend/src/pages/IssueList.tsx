import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Table,
  Button,
  Space,
  Tag,
  Input,
  Select,
  Card,
  message
} from 'antd'
import { PlusOutlined, SearchOutlined } from '@ant-design/icons'
import api from '../services/api'

const { Search } = Input
const { Option } = Select

const IssueList: React.FC = () => {
  const navigate = useNavigate()
  const [issues, setIssues] = useState([])
  const [loading, setLoading] = useState(false)
  const [filters, setFilters] = useState({
    status: undefined,
    priority: undefined,
    category: undefined,
    search: ''
  })

  useEffect(() => {
    loadIssues()
  }, [filters])

  const loadIssues = async () => {
    setLoading(true)
    try {
      const params: any = {}
      if (filters.status) params.status = filters.status
      if (filters.priority) params.priority = filters.priority
      if (filters.category) params.category = filters.category
      if (filters.search) params.search = filters.search

      const response = await api.get('/issues', { params })
      setIssues(response.data)
    } catch (error) {
      message.error('加载失败')
    } finally {
      setLoading(false)
    }
  }

  const statusColors: Record<string, string> = {
    open: 'blue',
    in_progress: 'orange',
    resolved: 'green',
    closed: 'default',
    rejected: 'red'
  }

  const priorityColors: Record<string, string> = {
    low: 'default',
    medium: 'blue',
    high: 'orange',
    urgent: 'red'
  }

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 60,
    },
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
      render: (text: string, record: any) => (
        <a onClick={() => navigate(`/issues/${record.id}`)}>{text}</a>
      ),
    },
    {
      title: '分类',
      dataIndex: 'category',
      key: 'category',
      width: 100,
      render: (category: string) => <Tag>{category}</Tag>,
    },
    {
      title: '优先级',
      dataIndex: 'priority',
      key: 'priority',
      width: 80,
      render: (priority: string) => (
        <Tag color={priorityColors[priority]}>{priority}</Tag>
      ),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: string) => (
        <Tag color={statusColors[status]}>{status}</Tag>
      ),
    },
    {
      title: 'AI标签',
      dataIndex: 'ai_tags',
      key: 'ai_tags',
      width: 200,
      render: (tags: string) => {
        if (!tags) return '-'
        return tags.split(',').map((tag: string, i: number) => (
          <Tag key={i} color="purple">{tag.trim()}</Tag>
        ))
      },
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (date: string) => new Date(date).toLocaleString('zh-CN'),
    },
  ]

  return (
    <div>
      <Card>
        <Space direction="vertical" size="middle" style={{ width: '100%' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <h1>问题管理</h1>
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={() => navigate('/issues/create')}
            >
              新建问题
            </Button>
          </div>

          <Space wrap>
            <Search
              placeholder="搜索问题"
              allowClear
              style={{ width: 300 }}
              onSearch={(value) => setFilters({ ...filters, search: value })}
            />
            
            <Select
              placeholder="状态"
              allowClear
              style={{ width: 120 }}
              onChange={(value) => setFilters({ ...filters, status: value })}
            >
              <Option value="open">待处理</Option>
              <Option value="in_progress">处理中</Option>
              <Option value="resolved">已解决</Option>
              <Option value="closed">已关闭</Option>
            </Select>

            <Select
              placeholder="优先级"
              allowClear
              style={{ width: 120 }}
              onChange={(value) => setFilters({ ...filters, priority: value })}
            >
              <Option value="low">低</Option>
              <Option value="medium">中</Option>
              <Option value="high">高</Option>
              <Option value="urgent">紧急</Option>
            </Select>

            <Select
              placeholder="分类"
              allowClear
              style={{ width: 120 }}
              onChange={(value) => setFilters({ ...filters, category: value })}
            >
              <Option value="bug">缺陷</Option>
              <Option value="feature">功能</Option>
              <Option value="improvement">改进</Option>
              <Option value="question">疑问</Option>
              <Option value="other">其他</Option>
            </Select>
          </Space>

          <Table
            columns={columns}
            dataSource={issues}
            rowKey="id"
            loading={loading}
            pagination={{
              pageSize: 20,
              showTotal: (total) => `共 ${total} 条`,
            }}
          />
        </Space>
      </Card>
    </div>
  )
}

export default IssueList



