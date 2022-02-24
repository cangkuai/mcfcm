package cn.ckapp.fcm;
import com.ejlchina.okhttps.HTTP;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;

public class chack implements Listener {
    @EventHandler
    public void chack(PlayerJoinEvent e){
        HTTP h=HTTP.builder().baseUrl("http://47.117.160.154:6100").build();
        String s= (String) h.sync("/api/?act={act}&user={user}&logins=t").addPathPara("act","chack").addPathPara("user",e.getPlayer().getName()).get().getBody().toString();
    if(s.equals("no")){
        e.getPlayer().kickPlayer("防沉迷系统：本日游玩时间已到达上限，如需继续游玩请完成实名认证");
    }
        }


}

