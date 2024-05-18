import discord 
import asyncio 
from discord.ext import commands 
from random import * 
import time 
import json

roles = [1221394719297245195]
db='../Bot/jsonfiles/polise_base.json'
db1='../Bot/jsonfiles/car_number.json'
status_role= [1224068990758817963,1224069202474831882,1224069115526774865]

class Modal2(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Тип рапорта"))
        self.add_item(discord.ui.InputText(label="Кому:"))
        self.add_item(discord.ui.InputText(label="От кого:"))
        self.add_item(discord.ui.InputText(label="Текст рапорта", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"Рапорт")
        embed.add_field(name="Тип рапорта", value=self.children[0].value)
        embed.add_field(name="Кому:", value=self.children[1].value)
        embed.add_field(name="От кого:", value=self.children[2].value)
        embed.add_field(name="Текст рапорта", value=self.children[3].value)
        await interaction.response.send_message(embeds=[embed])
        
class Modal_arrest(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Кому:"))
        self.add_item(discord.ui.InputText(label="Причина:"))
        self.add_item(discord.ui.InputText(label="Срок ареста:"))
        self.add_item(discord.ui.InputText(label="Штраф:"))

    async def callback(self, interaction: discord.Interaction):
         with open(db,'r',encoding='utf-8') as file:
              pb = json.load(file)
              if self.children[0].value not in pb:
                  await interaction.response.send_message('Такого гражданина нет в базе.')
              elif self.children[0].value in pb:
                with open(db,'w',encoding='utf-8') as file:
                    pb[f'{self.children[0].value}']["arrest"].append(f'По причине {self.children[1].value} арестован на срок {self.children[2].value} с суммой выплат {self.children[3].value}')
                    json.dump(pb,file)
                    await interaction.response.send_message(f'Гражданин {self.children[0].value} был арестован')

class Modal_fine(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Кому:"))
        self.add_item(discord.ui.InputText(label="Сумма штрафа:"))
        self.add_item(discord.ui.InputText(label="Штрафные поинты:"))
        self.add_item(discord.ui.InputText(label="Причина:"))

    async def callback(self, interaction: discord.Interaction):
        with open(db,'r',encoding='utf-8') as file:
              pb = json.load(file)
              if self.children[0].value not in pb:
                  await interaction.response.send_message('Такого гражданина нет в базе.')
              elif self.children[0].value in pb:
                with open(db,'w',encoding='utf-8') as file:
                    num =  pb[f'{self.children[0].value}']["points"]+ int(f'{self.children[2].value}')
                    pb[f'{self.children[0].value}']["fine"].append(f'{self.children[1].value} по причине {self.children[3].value}')
                    pb[f'{self.children[0].value}']["points"] = num
                    json.dump(pb,file)
                    await interaction.response.send_message(f'Гражданину {self.children[0].value} выдается штраф на сумму {self.children[1].value} и количеством штрафных поинтов {self.children[2].value} по причине {self.children[3].value}')     
         



class Modal4(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Гражданин"))

    async def callback(self, interaction: discord.Interaction):
         with open(db,'r',encoding='utf-8') as file:
              pb = json.load(file)
              if self.children[0].value not in pb:
                  await interaction.response.send_message('Такого гражданина нет в базе.')
              elif self.children[0].value in pb:

                md = ''
                for pos in pb[self.children[0].value]["fine"]:
                    md += f'{pos} \n'

                md1 = ''
                for pos1 in pb[self.children[0].value]["arrest"]:
                     md1 += f'{pos1} \n'

                embed = discord.Embed(title=f"{self.children[0].value}")
                embed.add_field(name = "Место проживания", value=pb[self.children[0].value]["domicile"], inline = False)
                embed.add_field(name = "Место работы", value=pb[self.children[0].value]["job"], inline = False)
                embed.add_field(name = "Имущество", value=pb[self.children[0].value]["Property"], inline = False)
                embed.add_field(name = "Лицензии", value=pb[self.children[0].value]["Licenses"], inline = False)
                embed.add_field(name = "Штрафы", value=md, inline = False)
                embed.add_field(name = "Аресты", value = md1, inline = False)
                embed.add_field(name = "Штрафные поинты", value=pb[self.children[0].value]["points"], inline = False)

                await interaction.response.send_message(embeds=[embed])

                
class Modal5(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Номер Автомобиля:"))

    async def callback(self, interaction: discord.Interaction):
         with open(db1,'r',encoding='utf-8') as file:
              cn = json.load(file)
              if self.children[0].value not in cn:
                  await interaction.response.send_message('Такого автомобиля нет в базе.')
              elif self.children[0].value in cn:
                embed = discord.Embed(title=f"{self.children[0].value}")
                embed.add_field(name="Владелец", value=cn[self.children[0].value]["owner"])
                embed.add_field(name="Модель", value=cn[self.children[0].value]["model"])
                embed.add_field(name="VIN номер", value=cn[self.children[0].value]["vin"])
                embed.add_field(name="Цвет", value=cn[self.children[0].value]["colour"])
                await interaction.response.send_message(embeds=[embed])
                          
class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)              
    #Рапорт            
    @discord.ui.button(label="Рапорт",row=0,style= discord.ButtonStyle.green)    
    async def button_callback2(self, button, interaction: discord.Integration):       
        await interaction.response.send_modal(Modal2(title="Рапорт:"))
    #Арест            
    @discord.ui.button(label="Арест гражданина",row=0, style= discord.ButtonStyle.green)
    async def button_callback_arrest(self, button, interaction: discord.Integration):        
        await interaction.response.send_modal(Modal_arrest(title='Аресты'))       
    #Выдача штрафов            
    @discord.ui.button(label="Выдача штрафов",row=0, style= discord.ButtonStyle.green)
    async def button_callback_fine(self, button, interaction: discord.Integration):        
        await interaction.response.send_modal(Modal_fine(title='Штрафы'))
    #Экстренная кнопка           
    @discord.ui.button(label="Кнопка паники",row=0,style= discord.ButtonStyle.red)    
    async def button_callback4(self, button, interaction: discord.Integration):        
        await interaction.response.send_message(f'<@&1203753862377250888> Офицеру <@{interaction.user.id}> необходима помощь.')
    #DB gr        
    @discord.ui.button(label="Поиск гражданина",row=1, style= discord.ButtonStyle.grey)
    async def button_callbac5(self, button, interaction: discord.Integration):        
        await interaction.response.send_modal(Modal4(title='Поиск граждан'))
    #DB car            
    @discord.ui.button(label="Поиск автомобильных номеров",row=1, style= discord.ButtonStyle.grey)
    async def button_callback6(self, button, interaction: discord.Integration):        
        await interaction.response.send_modal(Modal5(title='Поиск Автомобиля'))
    #Кнопки статуса
    @discord.ui.button(label="Досупен",row=2,style = discord.ButtonStyle.green)    
    async def button_callback_avail(self, button, interaction: discord.Integration):        
        if len(set([i.id for i in interaction.user.roles]) & set(status_role))>0:                
                for i in (set([i.id for i in interaction.user.roles]) & set(status_role)):
                    roles = interaction.guild.get_role(i)
                    await interaction.user.remove_roles(roles)
                    role = interaction.guild.get_role(1224068990758817963)
                    await interaction.user.add_roles(role)            
        elif len(set([i.id for i in interaction.user.roles]) & set(status_role))==0:
                role = interaction.guild.get_role(1224068990758817963)
                await interaction.user.add_roles(role)
    @discord.ui.button(label="Занят",row=2,style = discord.ButtonStyle.primary)    
    async def button_callback_busy(self, button, interaction: discord.Integration):        
        if len(set([i.id for i in interaction.user.roles]) & set(status_role))>0:                
                for i in (set([i.id for i in interaction.user.roles]) & set(status_role)):
                    roles = interaction.guild.get_role(i)
                    await interaction.user.remove_roles(roles)
                    role = interaction.guild.get_role(1224069115526774865)
                    await interaction.user.add_roles(role)            
        elif len(set([i.id for i in interaction.user.roles]) & set(status_role))==0:
                role = interaction.guild.get_role(1224069115526774865)
                await interaction.user.add_roles(role)    
    @discord.ui.button(label="Недоступен",row=2,style = discord.ButtonStyle.red)    
    async def button_callback_unavail(self, button, interaction: discord.Integration):        
        if len(set([i.id for i in interaction.user.roles]) & set(status_role))>0:                
                for i in (set([i.id for i in interaction.user.roles]) & set(status_role)):
                    roles = interaction.guild.get_role(i)
                    await interaction.user.remove_roles(roles)
                    role = interaction.guild.get_role(1224069202474831882)
                    await interaction.user.add_roles(role)            
        elif len(set([i.id for i in interaction.user.roles]) & set(status_role))==0:
                role = interaction.guild.get_role(1224069202474831882)
                await interaction.user.add_roles(role)         

class Police(commands.Cog):      
    def __init__(self, bot: discord.Bot) -> None:        
        super().__init__()        
        self.bot = bot    
        
    @discord.Cog.listener()    
    async def on_ready(self):        
        print('Модуль Police запушен')  	    
    
    @discord.command(description='Вызов меню')
    @commands.has_any_role(1053259873036550185,1224065876014268437,1151240778337763338,1155963751573495989,1153338699086569472,1203951479623254016,1182438539988832337)
    async def police(self,ctx):
        embed = discord.Embed()
        embed.set_image(url = "https://sun9-23.userapi.com/impf/3tRAzGJTXPTt-e9CDtl-ijIWJMvVJl_ov-MEGg/CRXa76TCrRs.jpg?size=1920x768&quality=95&crop=295,0,1000,399&sign=9155e4cf39b41f69d9285f825664e139&type=cover_group")
        await ctx.respond(embed = embed, view=Buttons(), ephemeral = True)
               
def setup(bot):   
    bot.add_cog(Police(bot))