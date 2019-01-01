package cn.fraudmetrix.sphinx.biz.service.impl;

import cn.fraudmetrix.holmes.service.intf.ICalculateService;
import cn.fraudmetrix.holmes.service.object.ModelCalResponse;
import cn.fraudmetrix.module.common.tracer.ThreadContextUtil;
import cn.fraudmetrix.sphinx.biz.bo.behaviour.WebButtonClickBehaviour;
import cn.fraudmetrix.sphinx.biz.bo.behaviour.KeyboardEvent;
import cn.fraudmetrix.sphinx.biz.bo.behaviour.MouseEvent;
import cn.fraudmetrix.sphinx.biz.bo.behaviour.SlideBehaviour;
import cn.fraudmetrix.sphinx.biz.bo.result.UserBehaviourResult;
import cn.fraudmetrix.sphinx.biz.service.intf.UserBehaviourRiskModelService;
import com.alibaba.fastjson.JSON;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;

import java.io.*;
import java.util.*;

/**
 * Created by qi.sun on 2018/1/23.
 */
public class UserBehaviourRiskModelServiceImpl implements UserBehaviourRiskModelService {

    private static Logger     logger                  = LoggerFactory.getLogger(UserBehaviourRiskModelServiceImpl.class);
    private static Logger     businessLogger          = LoggerFactory.getLogger("businessLogger");
    private static String     PARAM_SEQ_ID            = "seq_id";
    private static String     PARAM_PARAMS            = "params";
    private static String     PARAM_EVENT_INFO        = "event_info";
    private static String     PARAM_TIME              = "Time";
    private static String     PARAM_KEY_EVENT_TYPE    = "key_event_type";

    private static String     PARAM_DIALOG_TYPE       = "dialog_type";
    private static String     PARAM_MOUSE_EVENT_TYPE  = "mouse_event_type";
    private static String     PARAM_EVENT_TYPE        = "event_type";

    private static String     PARAM_OP_X              = "op_x";
    private static String     PARAM_OP_Y              = "op_y";
    private static String     PARAM_ACTION            = "Action";
    private static String     PARAM_TRUE_INFO         = "true_info";
    private static String     PARAM_FIRST_X           = "first_x";
    private static String     PARAM_FIRST_Y           = "first_y";
    private static String     PARAM_SECOND_X          = "second_x";
    private static String     PARAM_SECOND_Y          = "second_y";
    private static String     PARAM_SCENARIO          = "scenario";
    private static String     PARAM_TERMINAL          = "terminal";
    private static String     PARAM_PARTNER_CODE      = "partner_code";
    private static String     PARAM_MODEL_UUID        = "model_uuid";

    // slide param
    private static String     PARAM_CORRECT_X         = "correct_x";
    private static String     PARAM_CORRECT_Y         = "correct_y";
    private static String     PARAM_SLIDE_BAR_LEFT_X  = "slidebarleft_x";
    private static String     PARAM_SLIDE_BAR_LEFT_Y  = "slidebarleft_y";
    private static String     PARAM_SLIDE_BAR_RIGHT_X = "slidebarright_x";
    private static String     PARAM_SLIDE_BAR_RIGHT_Y = "slidebarright_y";

    // 返回参数
    private static String     RESULT_PARAM_BOT        = "Bot";

    @Autowired
    private ICalculateService iCalculateService;
    private String            modelUUID;

    public void init() {
        try {
            logger.info("service init");
            BufferedReader bufferedReader = new BufferedReader(new FileReader(new File("/Users/sunqi/Desktop/testslide")));
            BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(new File("/Users/sunqi/Desktop/testslide-result")));
            while (true) {
                String line = bufferedReader.readLine();
                if (line == null) {
                    break;
                }
                if (StringUtils.isBlank(line)) {
                    continue;
                }
                SlideBehaviour slideBehaviour = JSON.parseObject(line, SlideBehaviour.class);
                bufferedWriter.write(JSON.toJSONString(geneSlideParamMap(slideBehaviour, "xin1")));
            }
            bufferedReader.close();
            bufferedWriter.close();
        } catch (Exception e) {
            logger.error("file exception", e);
        }
    }

    @Override
    public UserBehaviourResult calcButtonClick(WebButtonClickBehaviour beforeClickBehaviour, String partnerCode) {
        UserBehaviourResult userBehaviourResult = new UserBehaviourResult();
        try {
            Map<String, String> paramMap = geneButtonClickParamMap(beforeClickBehaviour, partnerCode);
            System.out.println(JSON.toJSONString(paramMap));
            ModelCalResponse modelCalResponse = iCalculateService.calculate(paramMap);
            if (modelCalResponse != null && modelCalResponse.isSuccess()) {
                userBehaviourResult.setSuccess(true);
                userBehaviourResult.setBotProbability(Float.parseFloat(modelCalResponse.getData().get(RESULT_PARAM_BOT).toString()));
            } else {
                userBehaviourResult.setSuccess(false);
                userBehaviourResult.setMsg(modelCalResponse == null ? "button click response null" : modelCalResponse.getReasonMsg());
            }
            businessLogger.info("userBehaviourResult:" + userBehaviourResult);
            logger.info("userBehaviourResult:" + userBehaviourResult);
        } catch (Exception e) {
            logger.error("calcButtonClick exception,traceId:" + ThreadContextUtil.getTraceId(), e);
            userBehaviourResult.setSuccess(false);
            userBehaviourResult.setMsg(e.getMessage());
        }

        return userBehaviourResult;
    }

    private Map<String, String> geneButtonClickParamMap(WebButtonClickBehaviour beforeClickBehaviour,
                                                        String partnerCode) {
        Map<String, String> paramMap = new HashMap<>();
        paramMap.put(PARAM_SEQ_ID, ThreadContextUtil.getTraceId());
        paramMap.put(PARAM_PARTNER_CODE, partnerCode);
        paramMap.put(PARAM_MODEL_UUID, modelUUID);

        Map<String, Object> verifyInfoMap = new HashMap<>();
        verifyInfoMap.put(PARAM_FIRST_X, beforeClickBehaviour.getButtonTopLeft().getX());
        verifyInfoMap.put(PARAM_FIRST_Y, beforeClickBehaviour.getButtonTopLeft().getY());
        verifyInfoMap.put(PARAM_SECOND_X, beforeClickBehaviour.getButtonLowerRight().getY());
        verifyInfoMap.put(PARAM_SECOND_Y, beforeClickBehaviour.getButtonLowerRight().getY());
        verifyInfoMap.put(PARAM_SCENARIO, beforeClickBehaviour.getScenario());
        verifyInfoMap.put(PARAM_TERMINAL, beforeClickBehaviour.getTerminal());
        paramMap.put(PARAM_TRUE_INFO, JSON.toJSONString(verifyInfoMap));
        long initialTimestamp = beforeClickBehaviour.getInitialTimeStamp();
        List<MouseEvent> mouseEventList = beforeClickBehaviour.getMouseEvents();
        List<KeyboardEvent> keyboardEventList = beforeClickBehaviour.getKeyboardEvents();
        List<EventInfo> eventInfoList = geneEventInfos(initialTimestamp, mouseEventList, keyboardEventList);
        Map<String, Object> eventInfoMap = geneEventInfoMap(eventInfoList, 0);
        paramMap.put(PARAM_EVENT_INFO, JSON.toJSONString(eventInfoMap));
        return paramMap;
    }

    @Override
    public UserBehaviourResult calcSlide(SlideBehaviour slideBehaviour, String partnerCode) {
        UserBehaviourResult userBehaviourResult = new UserBehaviourResult();
        try {
            Map<String, String> paramMap = geneSlideParamMap(slideBehaviour, partnerCode);
            System.out.println(JSON.toJSONString(paramMap));
            ModelCalResponse modelCalResponse = iCalculateService.calculate(paramMap);
            if (modelCalResponse != null && modelCalResponse.isSuccess()) {
                userBehaviourResult.setSuccess(true);
                userBehaviourResult.setBotProbability(Float.parseFloat(modelCalResponse.getData().get(RESULT_PARAM_BOT).toString()));
            } else {
                userBehaviourResult.setSuccess(false);
                userBehaviourResult.setMsg(modelCalResponse == null ? "response null" : modelCalResponse.getReasonMsg());
                logger.error("bad modelCalResponse : " + modelCalResponse);
            }
            businessLogger.info("userBehaviourResult:" + userBehaviourResult);
            logger.info("userBehaviourResult:" + userBehaviourResult);
        } catch (Exception e) {
            logger.error("slide model exception", e);
            userBehaviourResult.setSuccess(false);
            userBehaviourResult.setMsg(e.getMessage());
        }

        return userBehaviourResult;
    }

    private Map<String, String> geneSlideParamMap(SlideBehaviour slideBehaviour, String partnerCode) {
        Map<String, String> paramMap = new HashMap<>();
        paramMap.put(PARAM_SEQ_ID, ThreadContextUtil.getTraceId());
        paramMap.put(PARAM_PARTNER_CODE, partnerCode);
        paramMap.put(PARAM_MODEL_UUID, modelUUID);
        Map<String, Object> verifyInfoMap = new HashMap<>();
        verifyInfoMap.put(PARAM_CORRECT_X, slideBehaviour.getCorrectX());
        verifyInfoMap.put(PARAM_CORRECT_Y, slideBehaviour.getCorrectY());
        verifyInfoMap.put(PARAM_SLIDE_BAR_LEFT_X, slideBehaviour.getSlideBarTopLeft().getX());
        verifyInfoMap.put(PARAM_SLIDE_BAR_LEFT_Y, slideBehaviour.getSlideBarTopLeft().getY());
        verifyInfoMap.put(PARAM_SLIDE_BAR_RIGHT_X, slideBehaviour.getSlideBarLowerRight().getX());
        verifyInfoMap.put(PARAM_SLIDE_BAR_RIGHT_Y, slideBehaviour.getSlideBarLowerRight().getY());
        verifyInfoMap.put(PARAM_TERMINAL, slideBehaviour.getTerminal());
        verifyInfoMap.put(PARAM_SCENARIO, slideBehaviour.getScenario());
        paramMap.put(PARAM_TRUE_INFO, JSON.toJSONString(verifyInfoMap));
        long initialTimestamp = slideBehaviour.getInitialTimeStamp();
        List<MouseEvent> mouseEventList = slideBehaviour.getMouseEvents();
        List<EventInfo> eventInfoList = geneEventInfos(initialTimestamp, mouseEventList, null);
        Map<String, Object> eventInfoMap = geneEventInfoMap(eventInfoList, 1);
        paramMap.put(PARAM_EVENT_INFO, JSON.toJSONString(eventInfoMap));
        return paramMap;
    }

    /**
     * type 0 点击Button; type 1 滑动
     * 
     * @param eventInfoList
     * @param type
     * @return
     */
    private Map<String, Object> geneEventInfoMap(List<EventInfo> eventInfoList, int type) {
        List<Long> timeList = new ArrayList<>();
        List<Integer> keyEventTypeList = new ArrayList<>();
        List<Integer> dialogTypeList = new ArrayList<>();
        List<Integer> mouseEventTypeList = new ArrayList<>();
        List<Integer> xList = new ArrayList<>();
        List<Integer> yList = new ArrayList<>();
        List<String> actionList = new ArrayList<>();
        eventInfoList.stream().forEachOrdered(eventInfo -> {
            timeList.add(eventInfo.getTimestamp());
            keyEventTypeList.add(eventInfo.getKeybordEventType());
            dialogTypeList.add(eventInfo.getDialogType());
            mouseEventTypeList.add(eventInfo.getMouseEventType());
            xList.add(eventInfo.getX());
            yList.add(eventInfo.getY());
            actionList.add(eventInfo.getAction());
        });
        Map<String, Object> eventInfoMap = new HashMap<>();
        eventInfoMap.put(PARAM_TIME, timeList);
        if (type == 0) {
            eventInfoMap.put(PARAM_KEY_EVENT_TYPE, keyEventTypeList);
        } else if (type == 1) {
            eventInfoMap.put(PARAM_EVENT_TYPE, keyEventTypeList);
        }

        if (type == 0) {
            eventInfoMap.put(PARAM_DIALOG_TYPE, dialogTypeList);
            eventInfoMap.put(PARAM_MOUSE_EVENT_TYPE, mouseEventTypeList);
        }
        eventInfoMap.put(PARAM_OP_X, xList);
        eventInfoMap.put(PARAM_OP_Y, yList);
        eventInfoMap.put(PARAM_ACTION, actionList);
        return eventInfoMap;
    }

    private List<EventInfo> geneEventInfos(long initialTimestamp, List<MouseEvent> mouseEventList,
                                           List<KeyboardEvent> keyboardEventList) {
        List<EventInfo> eventInfoList = new ArrayList<>();
        if (mouseEventList != null) {
            mouseEventList.stream().forEach(mouseEvent -> {
                EventInfo eventInfo = new EventInfo();
                eventInfo.setTimestamp(mouseEvent.getTimestamp() + initialTimestamp);
                eventInfo.setX(mouseEvent.getPoint().getX());
                eventInfo.setY(mouseEvent.getPoint().getY());
                eventInfo.setMouseEventType(mouseEvent.getEventType());
                eventInfo.setAction(String.valueOf(mouseEvent.getAction()));
                eventInfoList.add(eventInfo);
            });
        }

        if (keyboardEventList != null) {
            keyboardEventList.stream().forEach(keyboardEvent -> {
                EventInfo eventInfo = new EventInfo();
                eventInfo.setTimestamp(keyboardEvent.getTimestamp() + initialTimestamp);
                eventInfo.setKeybordEventType(keyboardEvent.getEventType());
                eventInfo.setDialogType(keyboardEvent.getDialogEventType());
                eventInfoList.add(eventInfo);
            });
        }

        eventInfoList.sort((EventInfo e1,
                            EventInfo e2) -> Long.valueOf(e1.getTimestamp()).compareTo(Long.valueOf(e2.getTimestamp())));
        return eventInfoList;
    }

    public void setModelUUID(String modelUUID) {
        this.modelUUID = modelUUID;
    }

    class EventInfo {

        long   timestamp;
        int    keybordEventType;
        int    dialogType;
        int    mouseEventType;
        int    x;
        int    y;
        String action;

        public long getTimestamp() {
            return timestamp;
        }

        public void setTimestamp(long timestamp) {
            this.timestamp = timestamp;
        }

        public int getKeybordEventType() {
            return keybordEventType;
        }

        public void setKeybordEventType(int keybordEventType) {
            this.keybordEventType = keybordEventType;
        }

        public int getDialogType() {
            return dialogType;
        }

        public void setDialogType(int dialogType) {
            this.dialogType = dialogType;
        }

        public int getMouseEventType() {
            return mouseEventType;
        }

        public void setMouseEventType(int mouseEventType) {
            this.mouseEventType = mouseEventType;
        }

        public int getX() {
            return x;
        }

        public void setX(int x) {
            this.x = x;
        }

        public int getY() {
            return y;
        }

        public void setY(int y) {
            this.y = y;
        }

        public String getAction() {
            return action;
        }

        public void setAction(String action) {
            this.action = action;
        }
    }

}
