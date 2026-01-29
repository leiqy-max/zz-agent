1️⃣ 技术栈层面
层	技术	状态
OS	Linux / WSL / 企业内网可迁移	✅
LLM	智谱 Embedding API	✅
Backend	Python + SQLAlchemy	✅
向量库	PostgreSQL + pgvector	✅
数据治理	用户 / 表 / sequence 权限	✅
RAG	文档入库链路	✅

2️⃣ 架构层面
┌────────────┐
│ 运维文档   │  txt / md / 手册
└─────┬──────┘
      ↓
┌────────────┐
│ 文档加载   │ loader.py
└─────┬──────┘
      ↓
┌────────────┐
│ 切分       │ splitter.py
└─────┬──────┘
      ↓
┌────────────┐
│ Embedding  │ 智谱 API
└─────┬──────┘
      ↓
┌────────────┐
│ pgvector   │ documents.embedding
└────────────┘

### 🛠️ 技术栈概览 前端 (Frontend)
- 核心框架 : React 19 + Vite 5 (极速构建与热更新)
- UI 样式 : Tailwind CSS (原子化 CSS，响应式布局)
- 交互与动画 : Framer Motion (流畅的 UI 动效), Lucide React (图标库)
- 功能组件 :
  - react-markdown : 渲染 Markdown 格式的 AI 回复
  - axios : 处理 HTTP 请求与拦截
- 语言 : JavaScript (ES6+) 后端 (Backend)
- Web 框架 : FastAPI (高性能 Python 异步框架) + Uvicorn (ASGI 服务器)
- 数据库 : PostgreSQL
  - 向量扩展 : pgvector (用于存储和检索文本向量)
  - ORM : SQLAlchemy 2.0 (数据库交互)
- 大模型 (LLM) :
  - 核心模型 : ZhipuAI (智谱 GLM-4 / GLM-4V)
  - 多模态 : 集成 GLM-4V 处理图片理解任务
  - 工具链 : LangChain (辅助文本切分与处理), Pydantic (数据验证)
- 环境管理 : Python-dotenv
### ✨ 项目核心特点
1. RAG (检索增强生成) 架构
   
   - 知识库闭环 : 实现了“文档解析 -> 向量化存储 -> 语义检索 -> LLM 回答”的完整链路。
   - 严谨性控制 : 对于运维专业问题，严格限制仅基于检索到的文档回答，无文档时自动兜底转人工，避免“AI 幻觉”。
2. 智能意图识别与混合对话
   
   - 动态策略 : 后端内置意图判断逻辑，能区分**“闲聊” 与 “专业咨询”**。
   - 体验优化 : 闲聊时自然亲切，无需引用文档；专业问答时严谨规范，必须提供引用来源。
3. 多模态支持 (Multimodal)
   
   - 支持 图片上传与粘贴 ，集成了视觉大模型 (GLM-4V)，允许用户针对运维截图、架构图进行提问。
4. 极简与响应式 UI
   
   - 沉浸式体验 : 采用居中布局 ( max-w-3xl )，去除多余侧边栏，聚焦对话内容。
   - 流式交互 : 界面支持 Markdown 实时渲染和代码高亮，适配移动端与桌面端。
5. 工程化设计
   
   - 模块化 : 后端采用 Factory 模式封装 LLM 客户端，便于未来扩展其他模型 (如 Ollama, OpenAI)。
   - 配置化 : 通过环境变量 ( .env ) 管理 API Key 和模型参数，通过 Docker/Shell 脚本管理服务启停。

6. 如何迁移至内网（操作步骤）
第一步：准备环境 在内网服务器上安装 Docker 和 Docker Compose。

第二步：启动服务 将整个项目拷贝到内网，执行：

```
docker-compose up -d
```
这会自动启动数据库、Ollama 和应用服务。

第三步：导入知识 将您的运维文档（Word/PDF/Txt）放入服务器某个目录（例如 /data/docs ），执行：

```
python import_docs.py --dir /data/docs
```
这会自动解析文档、生成向量并存储到数据库。