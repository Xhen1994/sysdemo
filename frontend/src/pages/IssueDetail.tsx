import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Card,
  Descriptions,
  Tag,
  Button,
  Space,
  Modal,
  Form,
  Select,
  Input,
  Rate,
  Divider,
  List,
  Avatar,
  message,
  Spin
} from 'antd'
import {
  EditOutlined,
  DeleteOutlined,
  CommentOutlined,
  RobotOutlined,
  StarOutlined
} from '@ant-design/icons'
import api from '../services/api'

const { TextArea } = Input
const { Option } = Select

const IssueDetail: React.FC = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [issue, setIssue] = useState<any>(null)
  const [comments, setComments] = useState([])
  const [feedbacks, setFeedbacks] = useState([])
  const [loading, setLoading] = useState(false)
  const [updateModalVisible, setUpdateModalVisible] = useState(false)
  const [feedbackModalVisible, setFeedbackModalVisible] = useState(false)
  const [commentModalVisible, setCommentModalVisible] = useState(false)
  const [form] = Form.useForm()

  useEffect(() => {
    loadIssueDetail()
  }, [id])

  const loadIssueDetail = async () => {
    setLoading(true)
    try {
      const [issueRes, commentsRes, feedbacksRes] = await Promise.all([
        api.get(`/issues/${id}`),
        api.get(`/issues/${id}/comments`),
        api.get(`/issues/${id}/feedbacks`)
      ])
      setIssue(issueRes.data)
      setComments(commentsRes.data)
      setFeedbacks(feedbacksRes.data)
    } catch (error) {
      message.error('加载失败')
    } finally {
      setLoading(false)
    }
  }

  const handleUpdate = async (values: any) => {
    try {
      await api.put(`/issues/${id}`, values)
      message.success('更新成功')
      setUpdateModalVisible(false)
      loadIssueDetail()
    } catch (error) {
      message.error('更新失败')
    }
  }

  const handleDelete = () => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这个问题吗？',
      okText: '确定',
      cancelText: '取消',
      onOk: async () => {
        try {
          await api.delete(`/issues/${id}`)
          message.success('删除成功')
          navigate('/issues')
        } catch (error) {
          message.error('删除失败')
        }
      }
    })
  }

  const handleAddComment = async (values: any) => {
    try {
      await api.post(`/issues/${id}/comments`, null, {
        params: { content: values.content }
      })
      message.success('评论成功')
      setCommentModalVisible(false)
      form.resetFields()
      loadIssueDetail()
    } catch (error) {
      message.error('评论失败')
    }
  }

  const handleAddFeedback = async (values: any) => {
    try {
      await api.post('/issues/feedbacks', {
        ...values,
        issue_id: parseInt(id!)
      })
      message.success('反馈提交成功')
      setFeedbackModalVisible(false)
      form.resetFields()
      loadIssueDetail()
    } catch (error) {
      message.error('反馈提交失败')
    }
  }

  const handleAIReAnalyze = async () => {
    try {
      const response = await api.post(`/ai/analyze/${id}`)
      message.success('AI重新分析完成')
      loadIssueDetail()
    } catch (error) {
      message.error('AI分析失败')
    }
  }

  if (loading || !issue) {
    return <Spin size="large" style={{ display: 'block', margin: '100px auto' }} />
  }

  const statusColors: Record<string, string> = {
    open: 'blue',
    in_progress: 'orange',
    resolved: 'green',
    closed: 'default',
    rejected: 'red'
  }

  return (
    <div>
      <Card
        title={`问题详情 #${id}`}
        extra={
          <Space>
            <Button
              icon={<RobotOutlined />}
              onClick={handleAIReAnalyze}
            >
              AI重新分析
            </Button>
            <Button
              icon={<CommentOutlined />}
              onClick={() => setCommentModalVisible(true)}
            >
              添加评论
            </Button>
            <Button
              icon={<StarOutlined />}
              onClick={() => setFeedbackModalVisible(true)}
            >
              提交反馈
            </Button>
            <Button
              icon={<EditOutlined />}
              onClick={() => setUpdateModalVisible(true)}
            >
              编辑
            </Button>
            <Button
              danger
              icon={<DeleteOutlined />}
              onClick={handleDelete}
            >
              删除
            </Button>
          </Space>
        }
      >
        <Descriptions column={2} bordered>
          <Descriptions.Item label="标题" span={2}>
            {issue.title}
          </Descriptions.Item>
          <Descriptions.Item label="描述" span={2}>
            {issue.description}
          </Descriptions.Item>
          <Descriptions.Item label="分类">
            <Tag>{issue.category}</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="优先级">
            <Tag color={issue.priority === 'urgent' ? 'red' : 'blue'}>
              {issue.priority}
            </Tag>
          </Descriptions.Item>
          <Descriptions.Item label="状态">
            <Tag color={statusColors[issue.status]}>
              {issue.status}
            </Tag>
          </Descriptions.Item>
          <Descriptions.Item label="创建时间">
            {new Date(issue.created_at).toLocaleString('zh-CN')}
          </Descriptions.Item>
          <Descriptions.Item label="AI摘要" span={2}>
            {issue.ai_summary || '暂无'}
          </Descriptions.Item>
          <Descriptions.Item label="AI标签" span={2}>
            {issue.ai_tags ? (
              issue.ai_tags.split(',').map((tag: string, i: number) => (
                <Tag key={i} color="purple">{tag.trim()}</Tag>
              ))
            ) : '暂无'}
          </Descriptions.Item>
          <Descriptions.Item label="AI建议分类">
            {issue.ai_category_suggestion || '暂无'}
          </Descriptions.Item>
        </Descriptions>

        <Divider>评论</Divider>
        <List
          dataSource={comments}
          renderItem={(comment: any) => (
            <List.Item>
              <List.Item.Meta
                avatar={<Avatar>{comment.author_id}</Avatar>}
                title={`用户 #${comment.author_id}`}
                description={
                  <>
                    <div>{comment.content}</div>
                    <small style={{ color: '#999' }}>
                      {new Date(comment.created_at).toLocaleString('zh-CN')}
                    </small>
                  </>
                }
              />
            </List.Item>
          )}
        />

        <Divider>反馈</Divider>
        <List
          dataSource={feedbacks}
          renderItem={(feedback: any) => (
            <List.Item>
              <List.Item.Meta
                avatar={<Avatar>{feedback.author_id}</Avatar>}
                title={
                  <Space>
                    用户 #{feedback.author_id}
                    <Rate disabled defaultValue={feedback.rating} />
                  </Space>
                }
                description={
                  <>
                    <div>满意度: {feedback.is_satisfied ? '满意' : '不满意'}</div>
                    {feedback.content && <div>反馈: {feedback.content}</div>}
                    {feedback.improvement_suggestions && (
                      <div>改进建议: {feedback.improvement_suggestions}</div>
                    )}
                    <small style={{ color: '#999' }}>
                      {new Date(feedback.created_at).toLocaleString('zh-CN')}
                    </small>
                  </>
                }
              />
            </List.Item>
          )}
        />
      </Card>

      {/* 更新问题弹窗 */}
      <Modal
        title="更新问题"
        open={updateModalVisible}
        onCancel={() => setUpdateModalVisible(false)}
        footer={null}
      >
        <Form
          layout="vertical"
          onFinish={handleUpdate}
          initialValues={issue}
        >
          <Form.Item name="status" label="状态">
            <Select>
              <Option value="open">待处理</Option>
              <Option value="in_progress">处理中</Option>
              <Option value="resolved">已解决</Option>
              <Option value="closed">已关闭</Option>
            </Select>
          </Form.Item>
          <Form.Item name="priority" label="优先级">
            <Select>
              <Option value="low">低</Option>
              <Option value="medium">中</Option>
              <Option value="high">高</Option>
              <Option value="urgent">紧急</Option>
            </Select>
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              更新
            </Button>
          </Form.Item>
        </Form>
      </Modal>

      {/* 添加评论弹窗 */}
      <Modal
        title="添加评论"
        open={commentModalVisible}
        onCancel={() => setCommentModalVisible(false)}
        footer={null}
      >
        <Form form={form} layout="vertical" onFinish={handleAddComment}>
          <Form.Item
            name="content"
            rules={[{ required: true, message: '请输入评论内容' }]}
          >
            <TextArea rows={4} placeholder="请输入评论内容" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              提交评论
            </Button>
          </Form.Item>
        </Form>
      </Modal>

      {/* 提交反馈弹窗 */}
      <Modal
        title="提交反馈"
        open={feedbackModalVisible}
        onCancel={() => setFeedbackModalVisible(false)}
        footer={null}
      >
        <Form form={form} layout="vertical" onFinish={handleAddFeedback}>
          <Form.Item
            name="rating"
            label="评分"
            rules={[{ required: true, message: '请选择评分' }]}
          >
            <Rate />
          </Form.Item>
          <Form.Item
            name="is_satisfied"
            label="是否满意"
            rules={[{ required: true }]}
          >
            <Select>
              <Option value={true}>满意</Option>
              <Option value={false}>不满意</Option>
            </Select>
          </Form.Item>
          <Form.Item name="content" label="反馈内容">
            <TextArea rows={3} placeholder="请输入反馈内容" />
          </Form.Item>
          <Form.Item name="improvement_suggestions" label="改进建议">
            <TextArea rows={3} placeholder="请输入改进建议" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              提交反馈
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default IssueDetail



