const Discord = require("discord.js")
const dblclient = new Discord.Client()

const config = require("./config.json")

dblclient.on('ready', () => {
	console.log("Slavyori's Server count updated!")
})

const { stringify } = require('querystring')
const { request } = require('https')

const update = () => {
  const data = stringify({ server_count: dblclient.guilds.size })
  const req = request({
    host: 'discordbots.org',
    path: "/api/bots/" + dblclient.user.id +"/stats",
    method: 'POST',
    headers: {
      'Authorization': 'token-here',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Content-Length': Buffer.byteLength(data)
    }
  });
  req.write(data)
  req.end()
};

dblclient.on('ready', update)
dblclient.on('guildCreate', update)
dblclient.on('guildRemove', update)

dblclient.login(config.token)
