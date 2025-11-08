from telegram.ext import Application, MessageHandler, CommandHandler, filters
from telegram import Update
import os
import logging

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

#BOT_TOKEN = os.getenv('BOT_TOKEN')
#TARGET_CHAT_ID = os.getenv('TARGET_CHAT_ID')
BOT_TOKEN = '8086772851:AAFVr1EA0Au91Heps9lIth76zXCn5Uh6Adw'
TARGET_CHAT_ID = int("5068404869")


class ForwardBot:
    def __init__(self):
        self.target_chats = []  # 支持多个目标聊天
    
    async def start(self, update: Update, context):
        """启动命令"""
        await update.message.reply_text(
            "🤖 转发机器人已启动！\n"
            "我会将所有消息转发到预设的聊天。"
        )
    
    async def set_target(self, update: Update, context):
        """设置转发目标"""
        if context.args:
            chat_id = context.args[0]
            self.target_chats.append(chat_id)
            await update.message.reply_text(f"✅ 已添加转发目标: {chat_id}")
        else:
            await update.message.reply_text("请提供聊天ID: /set_target <chat_id>")
    
    async def forward_all_messages(self, update: Update, context):
        """转发所有消息到多个目标"""
        if not self.target_chats:
            await update.message.reply_text("⚠️ 请先设置转发目标: /set_target <chat_id>")
            return
        
        for chat_id in self.target_chats:
            try:
                await update.message.forward(chat_id=chat_id)
                logging.info(f"消息转发到 {chat_id}")
            except Exception as e:
                logging.error(f"转发到 {chat_id} 失败: {e}")
    
    async def forward_with_info(self, update: Update, context):
        """转发消息并添加来源信息"""
        if not TARGET_CHAT_ID:
            return
        
        user = update.message.from_user
        chat = update.message.chat
        
        # 创建信息文本
        info_text = (
            f"📨 来自: {user.first_name} (@{user.username})\n"
            f"💬 聊天: {chat.title if chat.title else '私聊'}\n"
            f"🆔 用户ID: {user.id}"
        )
        
        try:
            # 先转发原消息
            await update.message.forward(chat_id=TARGET_CHAT_ID)
            # 再发送来源信息
            await context.bot.send_message(
                chat_id=TARGET_CHAT_ID,
                text=info_text
            )
        except Exception as e:
            logging.error(f"转发失败: {e}")

def main():
    # 初始化机器人
    bot = ForwardBot()
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # 添加处理器
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("set_target", bot.set_target))
    
    # 选择一种转发方式：
    # 1. 简单转发
    application.add_handler(MessageHandler(
        filters.ALL & ~filters.COMMAND,
        bot.forward_all_messages
    ))
    
    # 2. 或者带来源信息的转发
    # application.add_handler(MessageHandler(
    #     filters.ALL & ~filters.COMMAND,
    #     bot.forward_with_info
    # ))
    
    print("🚀 转发机器人启动成功！")
    application.run_polling()

if __name__ == '__main__':
    main()
