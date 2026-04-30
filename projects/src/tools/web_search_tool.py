"""
联网搜索工具 - 用于搜索课程相关的学习资料
"""
from langchain.tools import tool
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context


@tool
def web_search(query: str, count: int = 5) -> str:
    """
    搜索互联网上的学习资料和课程相关信息。
    
    参数:
        query: 搜索关键词，可以是课程名称、概念、技术名词等
        count: 返回结果数量，默认5条
    
    返回:
        格式化的搜索结果，包含标题、来源、摘要和链接
    """
    ctx = new_context(method="web_search")
    client = SearchClient(ctx=ctx)
    
    try:
        response = client.web_search_with_summary(
            query=query,
            count=count
        )
        
        # 格式化输出搜索结果
        results = []
        results.append(f"搜索关键词: {query}")
        results.append(f"共找到 {len(response.web_items)} 条结果\n")
        
        for i, item in enumerate(response.web_items, 1):
            results.append(f"{i}. {item.title}")
            results.append(f"   来源: {item.site_name}")
            if item.snippet:
                results.append(f"   摘要: {item.snippet[:200]}...")
            if item.url:
                results.append(f"   链接: {item.url}")
            results.append("")
        
        return "\n".join(results)
        
    except Exception as e:
        return f"搜索失败: {str(e)}"
