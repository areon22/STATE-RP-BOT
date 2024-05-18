import discord
import asyncio
from discord.ext import commands
from random import *
import time
import json

roles = [1221394719297245195]
db='C:/Users/Пуля/Desktop/Bot/jsonfiles/polise_base.json'
db1 = 'C:/Users/Пуля/Desktop/Bot/jsonfiles/car_number.json'

class PB(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Имя Фамилия"))
        self.add_item(discord.ui.InputText(label="Место проживания"))
        self.add_item(discord.ui.InputText(label="Место работы"))
        self.add_item(discord.ui.InputText(label="Имущесво"))
        self.add_item(discord.ui.InputText(label="Лицензии"))

    async def callback(self, interaction: discord.Interaction):
            with open(db,'r',encoding='utf-8') as file:
              new_users = json.load(file)
              with open(db,'w',encoding='utf-8') as file:
                  new_users[f'{self.children[0].value}'] = {'domicile':f'{self.children[1].value}',
                                                            "job":f'{self.children[2].value}',
                                                            "Property": f'{self.children[3].value}',
                                                            "Licenses":f'{self.children[4].value}',
                                                            'fine':[],
                                                            "arrest":[],
                                                            "points": 0 
                                                            }
                  json.dump(new_users,file)
                  await interaction.response.send_message(f'> Пользователь **{self.children[0].value}** внесен в базу.')

class CN(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Номер Автомобиля:"))
        self.add_item(discord.ui.InputText(label="Владелец:"))
        self.add_item(discord.ui.InputText(label="Марка и модель:"))
        self.add_item(discord.ui.InputText(label="VIN:"))
        self.add_item(discord.ui.InputText(label="Цвет:"))

    async def callback(self, interaction: discord.Interaction):
            with open(db1,'r',encoding='utf-8') as file:
              car = json.load(file)
              with open(db1,'w',encoding='utf-8') as file:
                  car[f'{self.children[0].value}'] = {'owner':f'{self.children[1].value}',
                                                            "model":f'{self.children[2].value}',
                                                            "colour": f'{self.children[4].value}',
                                                            "vin": f'{self.children[3].value}'
                                                            }
                  json.dump(car,file)
                  await interaction.response.send_message(f'Автомобиль с номерным знаком {self.children[0].value} зарегестирован.')


class Edit_car_number(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Какой номер:"))
        self.add_item(discord.ui.InputText(label="Какой пункт:"))
        self.add_item(discord.ui.InputText(label="На что:"))
    
    async def callback(self, interaction: discord.Interaction):
            with open(db1,'r',encoding='utf-8') as file:
              car = json.load(file)
              with open(db1,'w',encoding='utf-8') as file:
                    car[f'{self.children[0].value}'][self.children[1].value] = f'{self.children[2].value}'
                    json.dump(car,file)
                    await interaction.response.send_message(f'Автомобильный номер изменен')

class Edit_CIV(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Гражданин:"))
        self.add_item(discord.ui.InputText(label="Какой пункт:"))
        self.add_item(discord.ui.InputText(label="На что:"))
    
    async def callback(self, interaction: discord.Interaction):
            with open(db,'r',encoding='utf-8') as file:
              car = json.load(file)
              with open(db,'w',encoding='utf-8') as file:
                    car[f'{self.children[0].value}'][self.children[1].value] = f'{self.children[2].value}'
                    json.dump(car,file)
                    await interaction.response.send_message(f'Данные гражданина изменены')

class Edit_menu(discord.ui.View):
    @discord.ui.select(placeholder = "Выберете базу редактирования:",        
                       min_values = 1,        
                       max_values = 1,        
                       options = [discord.SelectOption(                
                           label="Автомобильные номера",                
                           description="База автомобильных номеров",
                            ),            
                                  discord.SelectOption(                
                           label="Граждане штата",                
                           description="База Граждан")                  
                                  ]    
                       )    
    async def select_callback(self, select, interaction):
        if select.values[0] == 'Автомобильные номера':
            await interaction.response.send_modal(Edit_car_number(title = "Внесение изменений"))
            
        if select.values[0] == 'Граждане штата':
            await interaction.response.send_modal(Edit_CIV(title = "Внесение изменений"))

class v911(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Служба:"))
        self.add_item(discord.ui.InputText(label="От кого:"))
        self.add_item(discord.ui.InputText(label="Место вызова:"))
        self.add_item(discord.ui.InputText(label="Причина вызова:"))
        self.add_item(discord.ui.InputText(label="Подробное описание ситуации:"))

    async def callb(self, interaction: discord.Interaction):
        emb = discord.Embed(description = f"Причина вызова:{self.children[3].value}")
        emb.set_author(name = f'От {self.children[1].value}')
        emb.add_field(name = f"Место вызова", value = f'{self.children[2].value}', inline =True)
        emb.add_field(name = f"Подробное описание ситуации", value = f'{self.children[4].value}', inline =True)
        await interaction.response.send_message(embed=emb)

class RP(commands.Cog):  
    def __init__(self, bot: discord.Bot) -> None:
        super().__init__()
        self.bot = bot

    @discord.Cog.listener()
    async def on_ready(self):
        print('Модуль RP запушен')

    @discord.command(description='Команда случайным образом выдает удачно или неудачно.')
    async def tryr(self,ctx):
        random_int = randint(1,20)
        if random_int<=10:
            await ctx.respond('> **Неудачно**')
        else:
            await ctx.respond('> **Удачно**')

    @discord.command(description='Команда случайным образом выдает число.')
    async def random(self,ctx,num:int):
        num = randint(1,int(num))
        await ctx.respond(f'> :game_die: Ты получил число: **{num}**')
        if num == None:
            await ctx.respond(randint(1,10))

    @discord.command(description="Команда предназначеная для внесения игрока в полицейскую базу")
    @commands.has_any_role(1187739137978150982,1053259873036550185,1224065876014268437,1151240778337763338)
    async def pb(self,ctx):
       await ctx.response.send_modal(PB(title="Внесение гражданина в базу"))
       
    @discord.command(description="Команда предназначеная для внесения машины в полицейскую базу")
    @commands.has_any_role(1187739137978150982,1053259873036550185,1224065876014268437,1151240778337763338,1155963751573495989,1153338699086569472,1203951479623254016,1182438539988832337)
    async def car_number(self,ctx):
       await ctx.response.send_modal(CN(title="Внесение авто в базу"))

    @discord.command(description = "Редакция базы данных")
    @commands.has_any_role(1187739137978150982,1053259873036550185,1224065876014268437,1151240778337763338)
    async def edit(self,ctx):
        await ctx.response.send_message(view = Edit_menu(), ephemeral = True)

    @discord.command(description = "Вызов 911")
    async def call(self,ctx):
        await ctx.response.send_modal(v911(title="Вызов 911"))
     
def setup(bot):
   bot.add_cog(RP(bot))
