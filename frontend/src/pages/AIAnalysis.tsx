import React, { useState } from 'react'
import {
  Card,
  Button,
  Spin,
  List,
  Typography,
  Row,
  Col,
  Statistic,
  message,
  Space
} from 'antd'
import { RobotOutlined, BulbOutlined, LineChartOutlined } from '@ant-design/icons'
import api from '../services/api'

const { Title, Paragraph, Text } = Typography

const AIAnalysis: React.FC = () => {
  const [loading, setLoading] = useState(false)
  const [analysis, setAnalysis] = useState<any>(null)

  const handleAnalyze = async () => {
    setLoading(true)
    try {
      const response = await api.get('/ai/trends', {
        params: { limit: 50 }
      })
      setAnalysis(response.data)
      message.success('AI分析完成')
    } catch (error) {
      message.error('分析失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <Card>
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div style={{ textAlign: 'center' }}>
            <Title level={2}>
              <RobotOutlined /> AI智能分析
            </Title>
            <Paragraph>
              使用人工智能技术分析问题趋势，提供智能洞察和改进建议
            </Paragraph>
            <Button
              type="primary"
              size="large"
              icon={<LineChartOutlined />}
              onClick={handleAnalyze}
              loading={loading}
            >
              开始分析
            </Button>
          </div>

          {loading && (
            <div style={{ textAlign: 'center', padding: '60px 0' }}>
              <Spin size="large" />
              <Paragraph style={{ marginTop: 20 }}>
                AI正在分析中，请稍候...
              </Paragraph>
            </div>
          )}

          {analysis && !loading && (
            <>
              <Card title="📊 数据统计" bordered={false}>
                <Row gutter={16}>
                  <Col span={6}>
                    <Statistic
                      title="分析问题总数"
                      value={analysis.statistics?.total || 0}
                    />
                  </Col>
                  <Col span={6}>
                    <Statistic
                      title="待处理"
                      value={analysis.statistics?.by_status?.open || 0}
                      valueStyle={{ color: '#faad14' }}
                    />
                  </Col>
                  <Col span={6}>
                    <Statistic
                      title="处理中"
                      value={analysis.statistics?.by_status?.in_progress || 0}
                      valueStyle={{ color: '#ff7a45' }}
                    />
                  </Col>
                  <Col span={6}>
                    <Statistic
                      title="已完成"
                      value={
                        (analysis.statistics?.by_status?.resolved || 0) +
                        (analysis.statistics?.by_status?.closed || 0)
                      }
                      valueStyle={{ color: '#52c41a' }}
                    />
                  </Col>
                </Row>

                <Title level={4} style={{ marginTop: 24 }}>
                  问题分类分布
                </Title>
                <Row gutter={16}>
                  {analysis.statistics?.by_category &&
                    Object.entries(analysis.statistics.by_category).map(
                      ([category, count]: [string, any]) => (
                        <Col span={8} key={category}>
                          <Card size="small">
                            <Statistic
                              title={category}
                              value={count}
                              suffix="个"
                            />
                          </Card>
                        </Col>
                      )
                    )}
                </Row>
              </Card>

              <Card
                title={
                  <>
                    <BulbOutlined /> AI趋势洞察
                  </>
                }
                bordered={false}
              >
                <List
                  dataSource={analysis.insights}
                  renderItem={(item: string, index: number) => (
                    <List.Item>
                      <Text strong>{index + 1}. </Text>
                      <Text>{item}</Text>
                    </List.Item>
                  )}
                />
              </Card>

              <Card
                title={
                  <>
                    💡 AI改进建议
                  </>
                }
                bordered={false}
              >
                <List
                  dataSource={analysis.recommendations}
                  renderItem={(item: string, index: number) => (
                    <List.Item>
                      <List.Item.Meta
                        avatar={
                          <div
                            style={{
                              width: 32,
                              height: 32,
                              borderRadius: '50%',
                              background: '#1890ff',
                              color: '#fff',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              fontWeight: 'bold'
                            }}
                          >
                            {index + 1}
                          </div>
                        }
                        description={<Text>{item}</Text>}
                      />
                    </List.Item>
                  )}
                />
              </Card>
            </>
          )}
        </Space>
      </Card>
    </div>
  )
}

export default AIAnalysis



