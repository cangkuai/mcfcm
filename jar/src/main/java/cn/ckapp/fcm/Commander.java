package cn.ckapp.fcm;
import com.ejlchina.okhttps.HTTP;
import org.bukkit.Bukkit;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

import javax.annotation.ParametersAreNonnullByDefault;
import java.util.Collection;

public class Commander implements CommandExecutor {
    @Override
    @ParametersAreNonnullByDefault
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        final Collection<? extends Player> players = Bukkit.getOnlinePlayers();
        for (Player player : players) {
            String p=player.getName();
            HTTP h=HTTP.builder().baseUrl("http://47.117.160.154:6100").build();
            String s= (String) h.sync("/api/?act={act}&user={user}").addPathPara("act","chack").addPathPara("user",p).get().getBody().toString();
            if(s.equals("no")){
                player.kickPlayer("防沉迷系统：本日游玩时间已到达上限，如需继续游玩请完成实名认证");
            }
        }
        return false;
    }
}