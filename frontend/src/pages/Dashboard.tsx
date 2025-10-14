import React, { useState, useEffect } from 'react'
import { Card, Row, Col, Statistic, Table, Tag, Space, Button } from 'antd'
import {
  FileTextOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  ExclamationCircleOutlined,
  RobotOutlined
} from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

interface Statistics {
  total: number
  open: number
  in_progress: number
  resolved: number
  closed: number
  completion_rate: number
}

const Dashboard: React.FC = () => {
  const navigate = useNavigate()
  const [stats, setStats] = useState<Statistics | null>(null)
  const [recentIssues, setRecentIssues] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    setLoading(true)
    try {
      const [statsRes, issuesRes] = await Promise.all([
        api.get('/issues/stats/summary'),
        api.get('/issues?limit=10')
      ])
      setStats(statsRes.data)
      setRecentIssues(issuesRes.data)
    } catch (error) {
      console.error('加载数据失败', error)
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

  const statusLabels: Record<string, string> = {
    open: '待处理',
    in_progress: '处理中',
    resolved: '已解决',
    closed: '已关闭',
    rejected: '已拒绝'
  }

  const priorityColors: Record<string, string> = {
    low: 'default',
    medium: 'blue',
    high: 'orange',
    urgent: 'red'
  }

  const priorityLabels: Record<string, string> = {
    low: '低',
    medium: '中',
    high: '高',
    urgent: '紧急'
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
      title: '优先级',
      dataIndex: 'priority',
      key: 'priority',
      width: 80,
      render: (priority: string) => (
        <Tag color={priorityColors[priority]}>
          {priorityLabels[priority]}
        </Tag>
      ),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: string) => (
        <Tag color={statusColors[status]}>
          {statusLabels[status]}
        </Tag>
      ),
    },
    {
      title: 'AI摘要',
      dataIndex: 'ai_summary',
      key: 'ai_summary',
      ellipsis: true,
      render: (text: string) => text || '-',
    },
  ]

  return (
    <div>
      <h1 style={{ marginBottom: 24 }}>工作台</h1>

      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="问题总数"
              value={stats?.total || 0}
              prefix={<FileTextOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="待处理"
              value={stats?.open || 0}
              prefix={<ClockCircleOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="处理中"
              value={stats?.in_progress || 0}
              prefix={<ExclamationCircleOutlined />}
              valueStyle={{ color: '#ff7a45' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="完成率"
              value={stats?.completion_rate || 0}
              suffix="%"
              prefix={<CheckCircleOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
      </Row>

      <Card
        title="最近问题"
        style={{ marginTop: 24 }}
        extra={
          <Space>
            <Button
              type="primary"
              icon={<RobotOutlined />}
              onClick={() => navigate('/ai-analysis')}
            >
              AI分析
            </Button>
            <Button type="primary" onClick={() => navigate('/issues/create')}>
              新建问题
            </Button>
          </Space>
        }
      >
        <Table
          columns={columns}
          dataSource={recentIssues}
          rowKey="id"
          loading={loading}
          pagination={false}
        />
      </Card>
    </div>
  )
}

export default Dashboard



