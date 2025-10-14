import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Card,
  Form,
  Input,
  Select,
  Button,
  message,
  Space,
  Spin
} from 'antd'
import { RobotOutlined } from '@ant-design/icons'
import api from '../services/api'

const { TextArea } = Input
const { Option } = Select

const IssueCreate: React.FC = () => {
  const [form] = Form.useForm()
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [aiLoading, setAiLoading] = useState(false)
  const [departments, setDepartments] = useState([])
  const [projects, setProjects] = useState([])
  const [users, setUsers] = useState([])

  useEffect(() => {
    loadOptions()
  }, [])

  const loadOptions = async () => {
    try {
      const [deptRes, projRes, userRes] = await Promise.all([
        api.get('/departments'),
        api.get('/projects'),
        api.get('/users')
      ])
      setDepartments(deptRes.data)
      setProjects(projRes.data)
      setUsers(userRes.data)
    } catch (error) {
      console.error('加载选项失败', error)
    }
  }

  const handleAIAnalyze = async () => {
    const title = form.getFieldValue('title')
    const description = form.getFieldValue('description')

    if (!title || !description) {
      message.warning('请先填写标题和描述')
      return
    }

    setAiLoading(true)
    try {
      const response = await api.post('/ai/summarize', {
        text: `${title}\n\n${description}`,
        max_length: 200
      })

      message.success('AI分析完成')
      message.info(`AI建议分类: ${response.data.category_suggestion || '无'}`)
      message.info(`AI标签: ${response.data.tags.join(', ')}`)
      
      // 可以选择自动填充AI建议的分类
      if (response.data.category_suggestion) {
        form.setFieldsValue({ category: response.data.category_suggestion })
      }
    } catch (error) {
      message.error('AI分析失败')
    } finally {
      setAiLoading(false)
    }
  }

  const onFinish = async (values: any) => {
    setLoading(true)
    try {
      const response = await api.post('/issues', values)
      message.success('问题创建成功，AI正在分析...')
      navigate(`/issues/${response.data.id}`)
    } catch (error) {
      message.error('创建失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <Card
        title="新建问题"
        extra={
          <Space>
            <Button onClick={() => navigate('/issues')}>取消</Button>
          </Space>
        }
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={{
            category: 'other',
            priority: 'medium'
          }}
        >
          <Form.Item
            name="title"
            label="问题标题"
            rules={[
              { required: true, message: '请输入问题标题' },
              { min: 5, message: '标题至少5个字符' }
            ]}
          >
            <Input placeholder="请输入简洁的问题标题" />
          </Form.Item>

          <Form.Item
            name="description"
            label="问题描述"
            rules={[
              { required: true, message: '请输入问题描述' },
              { min: 10, message: '描述至少10个字符' }
            ]}
          >
            <TextArea
              rows={6}
              placeholder="请详细描述问题的具体情况、影响范围等"
            />
          </Form.Item>

          <Space style={{ marginBottom: 16 }}>
            <Button
              icon={<RobotOutlined />}
              onClick={handleAIAnalyze}
              loading={aiLoading}
            >
              AI智能分析
            </Button>
          </Space>

          <Form.Item
            name="category"
            label="问题分类"
            rules={[{ required: true }]}
          >
            <Select>
              <Option value="bug">缺陷</Option>
              <Option value="feature">功能需求</Option>
              <Option value="improvement">改进建议</Option>
              <Option value="question">疑问咨询</Option>
              <Option value="other">其他</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="priority"
            label="优先级"
            rules={[{ required: true }]}
          >
            <Select>
              <Option value="low">低</Option>
              <Option value="medium">中</Option>
              <Option value="high">高</Option>
              <Option value="urgent">紧急</Option>
            </Select>
          </Form.Item>

          <Form.Item name="department_id" label="相关部门">
            <Select placeholder="选择部门" allowClear>
              {departments.map((dept: any) => (
                <Option key={dept.id} value={dept.id}>
                  {dept.name}
                </Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item name="project_id" label="关联项目">
            <Select placeholder="选择项目" allowClear>
              {projects.map((proj: any) => (
                <Option key={proj.id} value={proj.id}>
                  {proj.name}
                </Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item name="assignee_id" label="指派给">
            <Select placeholder="选择负责人" allowClear>
              {users.map((user: any) => (
                <Option key={user.id} value={user.id}>
                  {user.full_name || user.username}
                </Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" loading={loading}>
                创建问题
              </Button>
              <Button onClick={() => navigate('/issues')}>
                取消
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </div>
  )
}

export default IssueCreate



