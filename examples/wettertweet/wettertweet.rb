require "rubygems"
require "sequel"
require "twitter_oauth"
require "yaml"

config = YAML.load_file(File.join(File.dirname(__FILE__), "config.yaml"))

client = TwitterOAuth::Client.new(
    :consumer_key => config["twitter"]["consumer_key"],
    :consumer_secret => config["twitter"]["consumer_secret"],
    :token => config["twitter"]["token"],
    :secret => config["twitter"]["secret"]
)

DB = Sequel.connect(:adapter=>:mysql, :host=>config["mysql"]["host"], :user=>config["mysql"]["user"], :password=>config["mysql"]["password"], :database=>config["mysql"]["database"])

actual = DB[:ws300].where{s9_temp != nil}.reverse_order(:time).first
thirty_mins_ago = DB[:ws300].where{s9_temp != nil}.where{time < (actual[:time]-(60*30))}.reverse_order(:time).first
yesterday = DB[:ws300].where{s9_temp != nil}.where{time < (actual[:time]-(60*60*24))}.reverse_order(:time).first

str_temp_now = "%.1f" % actual[:s9_temp]
diff = actual[:s9_temp]-thirty_mins_ago[:s9_temp]
str_temp_now_rel = case
    when diff.abs <= 0.2 then "→"
    when diff < -1.5 then "↓"
    when diff < -0.2 then "↘"
    when diff > 1.5 then "↑"
    when diff > 0.2 then "↗"
end rescue ""

rain_rel = actual[:rain_rel]
str_regen = case
    when rain_rel == 0 then ""
    when rain_rel <= 0.75 then ", Nieselregen"
    else ", Regen"
end

str_relative_yesterday = "%+.1f" % (actual[:s9_temp]-yesterday[:s9_temp]) if yesterday

tweet = "Es ist #{Time.now.strftime("%H:%M")}. Temperatur: #{str_temp_now_rel} #{str_temp_now}°C#{str_regen}."
tweet+= "\nVergleich zu gestern: #{str_relative_yesterday}°C." if yesterday

client.update(tweet, :lat=>config["twitter"]["place"]["lat"], :lon=>config["twitter"]["place"]["lon"], :place_id=>config["twitter"]["place"]["place_id"], :display_coordinates=>1)
